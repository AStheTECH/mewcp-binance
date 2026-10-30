"""Call runner: rate-limit breaker, admission gate and SDK clients for every Binance call."""

import logging
import math
import threading
import time
from typing import Any

from binance_common import errors as sdk_errors
from binance_common.configuration import ConfigurationRestAPI
from binance_common.constants import (
    DERIVATIVES_TRADING_COIN_FUTURES_REST_API_PROD_URL,
    DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL,
    SPOT_REST_API_PROD_URL,
)
from binance_common.signature import Signers
from binance_sdk_derivatives_trading_coin_futures.derivatives_trading_coin_futures import (
    DerivativesTradingCoinFutures,
)
from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import (
    DerivativesTradingUsdsFutures,
)
from binance_sdk_spot.spot import Spot
from pydantic import BaseModel

from .config import (
    DEFAULT_RETRY_AFTER_SECONDS,
    GATE_WAIT_SECONDS,
    MAX_CONCURRENT_CALLS,
    PUBLIC_CLIENTS_PER_PRODUCT,
    SDK_BACKOFF_MS,
    SDK_RETRIES,
    SDK_TIMEOUT_MS,
)

logger = logging.getLogger("binance-mcp.runner")

_PRODUCTS: dict[str, tuple[Any, str]] = {
    "spot": (Spot, SPOT_REST_API_PROD_URL),
    "usdm": (DerivativesTradingUsdsFutures, DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL),
    "coinm": (DerivativesTradingCoinFutures, DERIVATIVES_TRADING_COIN_FUTURES_REST_API_PROD_URL),
}
_SECURITY = {"NONE", "MARKET_DATA", "USER_DATA", "TRADE"}
_SIGNED = {"USER_DATA", "TRADE"}


class BinanceCallError(Exception):
    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        retriable: bool = False,
        retry_after: int | None = None,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code  # UPSTREAM_ERROR | RATE_LIMITED | BUSY | VALIDATION_ERROR
        self.message = message
        self.retriable = retriable
        self.retry_after = retry_after
        self.details = details


def family_for(product: str, path: str) -> str:
    if product == "spot":
        return "spot"
    if product in ("usdm", "coinm"):
        return "futures"
    raise ValueError("Unknown product")


# Breaker

_now = time.monotonic
_blocked_until: dict[str, float] = {}
_breaker_lock = threading.Lock()


def _blocked_for(family: str) -> int:
    with _breaker_lock:
        until = _blocked_until.get(family)
        if until is None:
            return 0
        remaining = until - _now()
        if remaining <= 0:
            del _blocked_until[family]
            return 0
        return math.ceil(remaining)


def _trip(family: str, retry_after: int | None) -> int:
    seconds = retry_after if retry_after and retry_after > 0 else DEFAULT_RETRY_AFTER_SECONDS
    with _breaker_lock:
        until = max(_blocked_until.get(family, 0.0), _now() + seconds)
        _blocked_until[family] = until
        remaining = max(1, math.ceil(until - _now()))
    logger.warning("breaker family=%s status=blocked retry_after=%d", family, remaining)
    return remaining


# Counters

_stats = {"in_flight": 0, "waiting": 0, "busy_rejections": 0, "breaker_blocks": 0}
_stats_lock = threading.Lock()


def _bump(key: str, delta: int = 1) -> None:
    with _stats_lock:
        _stats[key] += delta


def stats() -> dict[str, int]:
    with _stats_lock:
        return dict(_stats)


# Gate

_gate = threading.BoundedSemaphore(MAX_CONCURRENT_CALLS)


# Clients

_public_clients: dict[str, list[Any]] = {}
_public_next: dict[str, int] = {}
_public_lock = threading.Lock()
_signer_lock = threading.Lock()


def _new_client(
    product: str, api_key: str | None, private_key: str | None, passphrase: str | None
) -> Any:
    client_cls, base_url = _PRODUCTS[product]
    config = ConfigurationRestAPI(
        api_key=api_key,
        private_key=private_key,
        private_key_passphrase=passphrase,
        base_path=base_url,
        timeout=SDK_TIMEOUT_MS,
        retries=SDK_RETRIES,
        backoff=SDK_BACKOFF_MS,
    )
    client = client_cls(config_rest_api=config)
    client.rest_api  # builds the session and signer once, here
    return client


def _next_public_client(product: str) -> Any:
    with _public_lock:
        pool = _public_clients.get(product)
        if pool is None:
            pool = [_new_client(product, None, None, None) for _ in range(PUBLIC_CLIENTS_PER_PRODUCT)]
            _public_clients[product] = pool
        idx = _public_next.get(product, 0)
        _public_next[product] = (idx + 1) % len(pool)
        return pool[idx]


def warm_public_clients() -> None:
    for product in _PRODUCTS:
        try:
            _next_public_client(product)
        except Exception as exc:
            logger.error("warm product=%s status=error type=%s", product, type(exc).__name__)


def _build_signed_client(product: str, api_key: str, private_key: str, passphrase: str | None) -> Any:
    with _signer_lock:  # SDK key caches are class-level; a concurrent clear can break a load
        try:
            return _new_client(product, api_key, private_key, passphrase)
        except (ValueError, TypeError, IndexError):
            raise ValueError("Invalid private_key or private_key_passphrase") from None


def _clear_signer_caches() -> None:
    with _signer_lock:
        Signers.clear_ed25519_cache()
        Signers.clear_rsa_cache()


def _close_session(client: Any) -> None:
    try:
        session = getattr(client.rest_api, "_session", None)
        if session is not None:
            session.close()
    except Exception:
        logger.debug("session close failed")


def _check_private_key(private_key: str | None) -> str:
    if not isinstance(private_key, str) or not private_key.strip().startswith("-----BEGIN"):
        raise ValueError("private_key must be PEM text beginning with -----BEGIN")
    return private_key.strip()


# Result conversion


def _flatten(value: Any) -> Any:
    if isinstance(value, dict):
        if "one_of_schemas" in value:
            return _flatten(value.get("actual_instance"))  # SDK oneOf wrapper
        extra = value.pop("additional_properties", None)
        out = {k: _flatten(v) for k, v in value.items()}
        if isinstance(extra, dict):
            for k, v in extra.items():
                out.setdefault(k, _flatten(v))
        return out
    if isinstance(value, list):
        return [_flatten(v) for v in value]
    return value


def _to_plain(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _flatten(value.model_dump(by_alias=True, mode="json", exclude_none=True))
    if isinstance(value, list):
        return [_to_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: _to_plain(v) for k, v in value.items()}
    return value


# Error mapping


def _map_error(exc: sdk_errors.Error, family: str) -> BinanceCallError:
    message = getattr(exc, "error_message", None) or "Binance request failed"
    sdk_code = getattr(exc, "status_code", None)
    details = {"binance_code": sdk_code} if sdk_code is not None else None
    if isinstance(exc, sdk_errors.TooManyRequestsError):
        retry = _trip(family, exc.retry_after)
        return BinanceCallError(429, "RATE_LIMITED", message, True, retry, details)
    if isinstance(exc, sdk_errors.RateLimitBanError):
        retry = _trip(family, exc.retry_after)
        return BinanceCallError(418, "RATE_LIMITED", message, False, retry, details)
    if isinstance(exc, sdk_errors.BadRequestError):
        return BinanceCallError(400, "UPSTREAM_ERROR", message, False, None, details)
    if isinstance(exc, sdk_errors.UnauthorizedError):
        return BinanceCallError(401, "UPSTREAM_ERROR", message, False, None, details)
    if isinstance(exc, sdk_errors.ForbiddenError):
        return BinanceCallError(403, "UPSTREAM_ERROR", message, False, None, details)
    if isinstance(exc, sdk_errors.NotFoundError):
        return BinanceCallError(404, "UPSTREAM_ERROR", message, False, None, details)
    if isinstance(exc, sdk_errors.ClientError):
        return BinanceCallError(400, "UPSTREAM_ERROR", message, False, None, details)
    if isinstance(exc, sdk_errors.RequiredError):
        return BinanceCallError(400, "VALIDATION_ERROR", message, False, None, None)
    if isinstance(exc, sdk_errors.ServerError):
        details = {"http_status": sdk_code} if sdk_code is not None else None
        return BinanceCallError(502, "UPSTREAM_ERROR", message, True, None, details)
    if isinstance(exc, sdk_errors.NetworkError):
        # SDK text embeds the request URL (may carry a signature); keep it out of responses
        return BinanceCallError(503, "UPSTREAM_ERROR", "Network error while contacting Binance", True)
    return BinanceCallError(502, "UPSTREAM_ERROR", message, False, None, details)


# Entry point


def call(
    product: str,
    path: str,
    security: str,
    method: str,
    kwargs: dict[str, Any],
    api_key: str | None = None,
    private_key: str | None = None,
    private_key_passphrase: str | None = None,
) -> Any:
    if product not in _PRODUCTS:
        raise ValueError("Unknown product")
    if security not in _SECURITY:
        raise ValueError("Unknown security type")
    signed = security in _SIGNED
    if security != "NONE" and not api_key:
        raise ValueError("Missing api_key credential")
    pem = _check_private_key(private_key) if signed else None

    family = family_for(product, path)
    remaining = _blocked_for(family)
    if remaining:
        _bump("breaker_blocks")
        logger.warning("call method=%s family=%s status=blocked retry_after=%d", method, family, remaining)
        raise BinanceCallError(
            429, "RATE_LIMITED",
            f"Binance {family} requests are blocked after a rate-limit response. "
            f"Do not retry for {remaining} seconds.",
            True, remaining,
        )

    gate = _gate
    _bump("waiting")
    try:
        acquired = gate.acquire(timeout=GATE_WAIT_SECONDS)
    finally:
        _bump("waiting", -1)
    if not acquired:
        _bump("busy_rejections")
        logger.warning("call method=%s family=%s status=busy", method, family)
        raise BinanceCallError(503, "BUSY", "Server is busy. Retry shortly.", True, 1)

    started = time.monotonic()
    status = "ok"
    client = None
    per_request = security != "NONE"
    _bump("in_flight")
    try:
        if security == "NONE":
            client = _next_public_client(product)
        elif signed:
            client = _build_signed_client(product, api_key, pem, private_key_passphrase)
        else:
            client = _new_client(product, api_key, None, None)
        response = getattr(client.rest_api, method)(**kwargs)
        return _to_plain(response.data())
    except sdk_errors.Error as exc:
        status = type(exc).__name__
        raise _map_error(exc, family) from None
    except BaseException as exc:
        status = type(exc).__name__
        raise
    finally:
        try:
            if per_request and client is not None:
                _close_session(client)
            if signed:
                _clear_signer_caches()
        finally:
            _bump("in_flight", -1)
            gate.release()
            logger.info(
                "call method=%s family=%s status=%s duration_ms=%d",
                method, family, status, round((time.monotonic() - started) * 1000),
            )
