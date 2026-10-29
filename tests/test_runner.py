import asyncio
import logging
import threading

import pytest
from binance_common import errors as E
from pydantic import BaseModel, Field

from binance_mcp import credentials, runner, service
from binance_mcp.runner import BinanceCallError

PEM = "-----BEGIN PRIVATE KEY-----\nSECRETKEYBODY123\n-----END PRIVATE KEY-----"
PASS = "hunter2-passphrase"
APIKEY = "APIKEY-abc123"


def call(product="spot", security="NONE", method="ping", **kw):
    return runner.call(product, "/x", security, method, kw.pop("kwargs", {}), **kw)


def signed(product="spot", method="account", **kw):
    return runner.call(product, "/x", "USER_DATA", method, {}, api_key=APIKEY,
                       private_key=PEM, private_key_passphrase=PASS, **kw)


def raiser(exc):
    def handler(product, method, kwargs):
        raise exc
    return handler


class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


@pytest.fixture
def clock(monkeypatch):
    c = Clock()
    monkeypatch.setattr(runner, "_now", c)
    return c


# Gate

def _blocking_handler(sdk):
    started, release = threading.Event(), threading.Event()

    def handler(product, method, kwargs):
        started.set()
        assert release.wait(5)
        return {"ok": True}

    sdk.handler = handler
    return started, release


def test_full_gate_returns_busy_without_sdk_call(sdk, monkeypatch):
    monkeypatch.setattr(runner, "_gate", threading.BoundedSemaphore(1))
    started, release = _blocking_handler(sdk)
    t = threading.Thread(target=call)
    t.start()
    assert started.wait(5)
    with pytest.raises(BinanceCallError) as ei:
        call()
    e = ei.value
    assert (e.status, e.code, e.retriable, e.retry_after) == (503, "BUSY", True, 1)
    assert len(sdk.calls) == 1
    assert runner.stats()["busy_rejections"] == 1
    release.set()
    t.join(5)


def test_slot_held_until_sdk_call_ends(sdk, monkeypatch):
    gate = threading.BoundedSemaphore(1)
    monkeypatch.setattr(runner, "_gate", gate)
    started, release = _blocking_handler(sdk)
    t = threading.Thread(target=call)
    t.start()
    assert started.wait(5)
    assert gate.acquire(blocking=False) is False  # caller gone or waiting: slot still used
    release.set()
    t.join(5)
    assert gate.acquire(blocking=False) is True
    gate.release()
    assert runner.stats()["in_flight"] == 0


def test_slot_released_when_sdk_raises(sdk, monkeypatch):
    gate = threading.BoundedSemaphore(1)
    monkeypatch.setattr(runner, "_gate", gate)
    sdk.handler = raiser(RuntimeError("boom"))
    with pytest.raises(RuntimeError):
        call()
    sdk.handler = raiser(E.BadRequestError("bad", -1100))
    with pytest.raises(BinanceCallError):
        call()
    assert gate.acquire(blocking=False) is True


# Breaker

def test_429_blocks_family_and_next_call_fails_fast(sdk):
    sdk.handler = raiser(E.TooManyRequestsError("slow down", -1003, 30))
    with pytest.raises(BinanceCallError) as ei:
        call()
    e = ei.value
    assert (e.status, e.code, e.retriable, e.retry_after) == (429, "RATE_LIMITED", True, 30)
    assert e.details == {"binance_code": -1003}
    assert len(sdk.calls) == 1
    with pytest.raises(BinanceCallError) as ei:
        call()
    e = ei.value
    assert (e.status, e.code, e.retriable) == (429, "RATE_LIMITED", True)
    assert 0 < e.retry_after <= 30
    assert "spot" in e.message and str(e.retry_after) in e.message
    assert len(sdk.calls) == 1


def test_418_keeps_status_not_retriable_and_blocks(sdk):
    sdk.handler = raiser(E.RateLimitBanError("banned", -1003, 120))
    with pytest.raises(BinanceCallError) as ei:
        call()
    e = ei.value
    assert (e.status, e.code, e.retriable, e.retry_after) == (418, "RATE_LIMITED", False, 120)
    with pytest.raises(BinanceCallError) as ei:
        call()
    assert ei.value.status == 429
    assert len(sdk.calls) == 1


def test_block_lifts_after_retry_after(sdk, clock):
    sdk.handler = raiser(E.TooManyRequestsError("x", None, 10))
    with pytest.raises(BinanceCallError):
        call()
    sdk.handler = lambda *a: {"ok": 1}
    clock.t += 9.5
    with pytest.raises(BinanceCallError):
        call()
    assert len(sdk.calls) == 1
    clock.t += 1.0
    assert call() == {"ok": 1}
    assert len(sdk.calls) == 2


def test_missing_retry_after_uses_default(sdk, clock):
    sdk.handler = raiser(E.TooManyRequestsError("x", None, None))
    with pytest.raises(BinanceCallError) as ei:
        call()
    assert ei.value.retry_after == runner.DEFAULT_RETRY_AFTER_SECONDS == 60
    sdk.handler = lambda *a: {"ok": 1}
    clock.t += 59
    with pytest.raises(BinanceCallError):
        call()
    clock.t += 2
    assert call() == {"ok": 1}


def test_later_error_extends_never_shortens(clock):
    runner._trip("spot", 100)
    runner._trip("spot", 10)
    assert runner._blocked_for("spot") == 100
    clock.t += 50
    runner._trip("spot", 100)
    assert runner._blocked_for("spot") == 100
    runner._trip("spot", 20)
    assert runner._blocked_for("spot") == 100


def test_spot_block_does_not_stop_futures_and_futures_share(sdk):
    sdk.handler = raiser(E.TooManyRequestsError("x", None, 30))
    with pytest.raises(BinanceCallError):
        call("spot")
    sdk.handler = lambda *a: {"ok": 1}
    assert call("usdm") == {"ok": 1}
    assert call("coinm") == {"ok": 1}
    sdk.handler = raiser(E.RateLimitBanError("x", None, 30))
    with pytest.raises(BinanceCallError):
        call("usdm")
    with pytest.raises(BinanceCallError) as ei:
        call("coinm")
    assert ei.value.status == 429 and "futures" in ei.value.message


def test_blocked_call_takes_no_gate_slot(sdk, monkeypatch):
    gate = threading.BoundedSemaphore(1)
    monkeypatch.setattr(runner, "_gate", gate)
    runner._trip("spot", 30)
    assert gate.acquire(blocking=False)  # gate full
    with pytest.raises(BinanceCallError) as ei:
        call()
    assert ei.value.code == "RATE_LIMITED"  # not BUSY
    s = runner.stats()
    assert s["breaker_blocks"] == 1 and s["waiting"] == 0 and s["busy_rejections"] == 0
    assert sdk.calls == []
    gate.release()


@pytest.mark.parametrize("exc,status,code,retriable", [
    (E.BadRequestError("m", -1121), 400, "UPSTREAM_ERROR", False),
    (E.UnauthorizedError("m", -2015), 401, "UPSTREAM_ERROR", False),
    (E.ForbiddenError("m", None), 403, "UPSTREAM_ERROR", False),
    (E.NotFoundError("m", None), 404, "UPSTREAM_ERROR", False),
    (E.ClientError("m"), 400, "UPSTREAM_ERROR", False),
    (E.RequiredError("symbol"), 400, "VALIDATION_ERROR", False),
    (E.ServerError("Server error: 503", 503), 502, "UPSTREAM_ERROR", True),
    (E.NetworkError("Network error: https://x/?signature=SIG"), 503, "UPSTREAM_ERROR", True),
])
def test_other_errors_map_and_never_trip_breaker(sdk, exc, status, code, retriable):
    sdk.handler = raiser(exc)
    with pytest.raises(BinanceCallError) as ei:
        call()
    e = ei.value
    assert (e.status, e.code, e.retriable, e.retry_after) == (status, code, retriable, None)
    assert "SIG" not in e.message
    sdk.handler = lambda *a: {"ok": 1}
    assert call() == {"ok": 1}


def test_binance_code_in_details(sdk):
    sdk.handler = raiser(E.BadRequestError("Invalid symbol.", -1121))
    with pytest.raises(BinanceCallError) as ei:
        call()
    assert ei.value.message == "Invalid symbol."
    assert ei.value.details == {"binance_code": -1121}


# Clients and credentials

def test_public_calls_use_shared_clients_without_credentials(sdk):
    for _ in range(7):
        call("spot")
    assert len(sdk.rest_apis) == runner.PUBLIC_CLIENTS_PER_PRODUCT
    for r in sdk.rest_apis:
        assert r.config.api_key is None and r.config.private_key is None
        assert r.config.api_secret is None
        assert r._session.closed is False
    assert len({id(r) for r in sdk.rest_apis}) == 3


def test_warm_public_clients_builds_per_product(sdk):
    runner.warm_public_clients()
    assert len(sdk.rest_apis) == 3 * 3
    before = len(sdk.rest_apis)
    call("usdm")
    assert len(sdk.rest_apis) == before


def test_market_data_sends_only_api_key_and_closes_session(sdk):
    runner.call("usdm", "/x", "MARKET_DATA", "m", {"a": 1}, api_key=APIKEY)
    (r,) = sdk.rest_apis
    assert r.config.api_key == APIKEY
    assert r.config.private_key is None and r.config.api_secret is None
    assert r._session.closed
    assert sdk.calls == [("usdm", "m", {"a": 1})]


def test_user_data_client_built_in_calling_thread_and_closed(sdk):
    out = {}

    def work():
        out["tid"] = threading.get_ident()
        signed()

    t = threading.Thread(target=work)
    t.start()
    t.join(5)
    (r,) = sdk.rest_apis
    assert r.created_in == out["tid"]
    assert r.config.api_key == APIKEY
    assert r.config.private_key == PEM
    assert r.config.private_key_passphrase == PASS
    assert r.config.api_secret is None
    assert r._session.closed


def test_signer_caches_cleared_after_signed_call_even_on_error(sdk):
    for exc in (None, E.BadRequestError("m", 1), RuntimeError("x")):
        runner.Signers._ed25519_keys[("k", None)] = object()
        runner.Signers._rsa_signers[("k", None)] = object()
        if exc is not None:
            sdk.handler = raiser(exc)
        try:
            signed()
        except Exception:
            pass
        assert not runner.Signers._ed25519_keys and not runner.Signers._rsa_signers
    assert all(r._session.closed for r in sdk.rest_apis)


@pytest.mark.parametrize("bad", [None, "", "/etc/passwd", "  not a pem", "BEGIN PRIVATE KEY"])
def test_bad_private_key_rejected_before_sdk(sdk, bad):
    with pytest.raises(ValueError) as ei:
        runner.call("spot", "/x", "USER_DATA", "account", {}, api_key=APIKEY, private_key=bad)
    assert "passwd" not in str(ei.value) and "not a pem" not in str(ei.value)
    assert sdk.rest_apis == [] and sdk.calls == []


def test_missing_api_key_rejected(sdk):
    with pytest.raises(ValueError):
        runner.call("spot", "/x", "MARKET_DATA", "m", {})
    assert sdk.rest_apis == []


def test_sdk_key_parse_error_is_generic(sdk, monkeypatch):
    def boom(*a, **k):
        raise ValueError("bad key text " + PEM)

    monkeypatch.setattr(runner, "_new_client", boom)
    with pytest.raises(ValueError) as ei:
        signed()
    assert "SECRETKEYBODY" not in str(ei.value)


def test_no_log_line_contains_secrets(sdk, caplog):
    caplog.set_level(logging.DEBUG)
    call()
    runner.call("spot", "/x", "MARKET_DATA", "m", {}, api_key=APIKEY)
    signed()
    for exc in (E.BadRequestError("m", 1), E.TooManyRequestsError("m", 1, 5)):
        sdk.handler = raiser(exc)
        with pytest.raises(BinanceCallError):
            signed()
    with pytest.raises(BinanceCallError):
        signed()  # blocked
    with pytest.raises(ValueError):
        runner.call("spot", "/x", "USER_DATA", "m", {}, api_key=APIKEY, private_key="x" + PEM)
    assert caplog.records
    text = "\n".join(r.getMessage() for r in caplog.records)
    for secret in (PEM, "SECRETKEYBODY", PASS, APIKEY, "X-MBX-APIKEY", "ConfigurationRestAPI"):
        assert secret not in text


# Conversion

class Inner(BaseModel):
    x: int | None = None
    additional_properties: dict = {}


class Outer(BaseModel):
    symbol_name: str = Field(alias="symbolName")
    inner: Inner
    items: list[Inner] = []
    none_field: str | None = None
    additional_properties: dict = {}


def test_to_plain_flattens_additional_properties(sdk):
    model = Outer(symbolName="BTC", inner=Inner(x=1, additional_properties={"y": 2}),
                  items=[Inner(x=3, additional_properties={"z": {"q": 1}})],
                  additional_properties={"extra": "e"})
    sdk.handler = lambda *a: model
    out = call()
    assert out == {"symbolName": "BTC", "inner": {"x": 1, "y": 2},
                   "items": [{"x": 3, "z": {"q": 1}}], "extra": "e"}
    sdk.handler = lambda *a: [model, {"raw": 1}]
    assert call()[1] == {"raw": 1}
    sdk.handler = lambda *a: [["a"], {"k": [1]}]
    assert call() == [["a"], {"k": [1]}]


class OneOf(BaseModel):
    actual_instance: Inner | list[Inner] | None = None
    one_of_schemas: set[str] = {"Inner"}
    oneof_schema_1_validator: Inner | None = None
    discriminator_value_class_map: dict = {}


class Holder(BaseModel):
    ref: OneOf
    additional_properties: dict = {}


def test_to_plain_unwraps_oneof(sdk):
    sdk.handler = lambda *a: OneOf(actual_instance=Inner(x=1, additional_properties={"y": 2}),
                                   oneof_schema_1_validator=Inner(x=1))
    assert call() == {"x": 1, "y": 2}
    sdk.handler = lambda *a: OneOf(actual_instance=[Inner(x=1), Inner(x=2)])
    assert call() == [{"x": 1}, {"x": 2}]
    sdk.handler = lambda *a: Holder(ref=OneOf(actual_instance=Inner(x=5)))
    assert call() == {"ref": {"x": 5}}


# Service

def test_service_drops_none_kwargs_and_skips_credentials_for_public(sdk, monkeypatch):
    def no_creds():
        raise AssertionError("credentials read for public call")

    monkeypatch.setattr(service, "get_credentials", no_creds)
    service.call("spot", "/api/v3/depth", "NONE", "depth", symbol="BTCUSDT", limit=5, x=None)
    assert sdk.calls == [("spot", "depth", {"symbol": "BTCUSDT", "limit": 5})]


class _Cred:
    def __init__(self, fields):
        self.fields = fields


def test_service_credential_checks(sdk, monkeypatch):
    fields = {}
    monkeypatch.setattr(service, "get_credentials", lambda: _Cred(fields))
    with pytest.raises(ValueError, match="Missing api_key credential"):
        service.call("spot", "/p", "MARKET_DATA", "m")
    fields["api_key"] = APIKEY
    service.call("spot", "/p", "MARKET_DATA", "m")
    with pytest.raises(ValueError, match="Missing private_key credential"):
        service.call("spot", "/p", "USER_DATA", "m")
    fields.update(private_key=PEM, private_key_passphrase=PASS)
    service.call("spot", "/p", "USER_DATA", "m")
    r = sdk.rest_apis[-1]
    assert r.config.private_key == PEM and r.config.private_key_passphrase == PASS
    assert r.config.api_secret is None


# Credential backend

def test_optional_static_backend():
    from fastmcp_credentials import MissingCredentialHeaderError, ResolvedCredential

    b = credentials.OptionalStaticBackend()

    async def missing(_):
        raise MissingCredentialHeaderError(["X-MCP-Cred-Fields"])

    b._headers.resolve = missing
    cred = asyncio.run(b.resolve("static"))
    assert cred.type == "static" and cred.fields == {}

    async def found(_):
        return ResolvedCredential(type="static", fields={"api_key": "k"})

    b._headers.resolve = found
    assert asyncio.run(b.resolve("static")).fields == {"api_key": "k"}
