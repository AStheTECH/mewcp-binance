"""Credential and call facade over the Binance call runner."""

import logging
from typing import Any

from fastmcp_credentials import get_credentials

from . import runner

logger = logging.getLogger("binance-mcp.service")


def _credentials(security: str) -> dict[str, str | None]:
    if security == "NONE":
        return {}
    fields = get_credentials().fields or {}
    api_key = fields.get("api_key")
    if not api_key:
        raise ValueError("Missing api_key credential")
    if security == "MARKET_DATA":
        return {"api_key": api_key}
    private_key = fields.get("private_key")
    if not private_key:
        raise ValueError("Missing private_key credential")
    return {
        "api_key": api_key,
        "private_key": private_key,
        "private_key_passphrase": fields.get("private_key_passphrase") or None,
    }


def call(product: str, path: str, security: str, method: str, **kwargs: Any) -> Any:
    params = {k: v for k, v in kwargs.items() if v is not None}
    return runner.call(product, path, security, method, params, **_credentials(security))
