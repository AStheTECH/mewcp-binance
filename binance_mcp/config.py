"""Configuration for MewCP Binance MCP Server."""

import logging
import os

SERVER_VERSION = "v1.0.0"
BREAKING_CHANGES: list[dict] = []

MAX_CONCURRENT_CALLS = 32  # admission gate size; kept below FastMCP's default 40 worker threads
GATE_WAIT_SECONDS = 5  # max wait for a gate slot before returning BUSY
PUBLIC_CLIENTS_PER_PRODUCT = 3  # shared credential-free SDK clients per product, round-robin
DEFAULT_RETRY_AFTER_SECONDS = 60  # block length when a 429/418 has no Retry-After; our default, not Binance's
SDK_TIMEOUT_MS = 1000  # SDK request timeout per step (SDK default)
SDK_RETRIES = 3  # SDK retries for GET/DELETE on 5xx and network errors (SDK default)
SDK_BACKOFF_MS = 1000  # SDK backoff step between retries (SDK default)


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
