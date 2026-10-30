"""Spot general group: get_spot_exchange_info, get_spot_execution_rules, get_spot_server_time, ping_spot"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.spot_general import (
    PingSpotData,
    PingSpotResult,
    SpotExchangeInfoData,
    SpotExchangeInfoResult,
    SpotExecutionRulesData,
    SpotExecutionRulesResult,
    SpotServerTimeData,
    SpotServerTimeResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("binance-mcp.tools.spot_general")

_SYMBOL_STATUSES = ("TRADING", "HALT", "BREAK", "CANCEL_ONLY")
_PERMISSIONS = ("SPOT", "MARGIN", "LEVERAGED") + tuple(f"TRD_GRP_{n:03d}" for n in range(2, 26))


def register_spot_general_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_spot_exchange_info",
        description=(
            "Returns Binance Spot exchange trading rules, rate limits and per-symbol information (status, assets, "
            "precisions, allowed order types, filters, permissions). With no filter the response covers every "
            "symbol and is very large, so pass symbol, symbols or permissions to narrow it; permissions cannot be "
            "combined with symbol or symbols, and symbol_status cannot be combined with symbol or symbols. "
            "An unknown symbol returns an invalid-symbol error. Request weight is 20."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_exchange_info(
        symbol: str | None = Field(default=None, description="Return info for a single symbol, e.g. ETHBTC. Optional."),
        symbols: list[str] | None = Field(
            default=None, description='Return info for multiple symbols, e.g. ["BTCUSDT", "BNBBTC"]. Optional.'
        ),
        permissions: list[str] | None = Field(
            default=None,
            description=(
                'Filter symbols by permission, e.g. ["SPOT"] or ["MARGIN", "LEVERAGED"]. Allowed values per item: '
                "SPOT, MARGIN, LEVERAGED, TRD_GRP_002 through TRD_GRP_025. Optional; without it, symbols with SPOT, "
                "MARGIN or LEVERAGED permission are returned, so list other permissions explicitly to include them."
            ),
        ),
        show_permission_sets: bool | None = Field(
            default=True,
            description="Controls whether the permissionSets field of each symbol is populated. Optional; Binance default is true.",
        ),
        symbol_status: str | None = Field(
            default=None,
            description="Return only symbols with this trading status: TRADING, HALT, BREAK or CANCEL_ONLY. Optional.",
        ),
    ) -> SpotExchangeInfoResult:
        tlog = ToolLogger(logger, "get_spot_exchange_info")

        if permissions is not None:
            bad = [p for p in permissions if p not in _PERMISSIONS]
            if bad:
                return _err(
                    SpotExchangeInfoResult, tlog, "VALIDATION_ERROR",
                    f"permissions contains unsupported values: {', '.join(bad)}", 400,
                )
            if symbol or symbols:
                return _err(
                    SpotExchangeInfoResult, tlog, "VALIDATION_ERROR",
                    "permissions cannot be combined with symbol or symbols", 400,
                )
        if symbol_status is not None:
            if symbol_status not in _SYMBOL_STATUSES:
                return _err(
                    SpotExchangeInfoResult, tlog, "VALIDATION_ERROR",
                    f"symbol_status must be one of {', '.join(_SYMBOL_STATUSES)}", 400,
                )
            if symbol or symbols:
                return _err(
                    SpotExchangeInfoResult, tlog, "VALIDATION_ERROR",
                    "symbol_status cannot be combined with symbol or symbols", 400,
                )

        try:
            data = service.call(
                "spot", "/api/v3/exchangeInfo", "NONE", "exchange_info",
                symbol=symbol or None,
                symbols=symbols or None,
                permissions=permissions or None,
                show_permission_sets=show_permission_sets,
                symbol_status=symbol_status,
            )
            tlog.success()
            return SpotExchangeInfoResult(success=True, statusCode=200, data=SpotExchangeInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotExchangeInfoResult, tlog, exc)

    @mcp.tool(
        name="get_spot_execution_rules",
        description=(
            "Returns the execution rules (such as price-range limits for bids and asks) for Binance Spot symbols. "
            "Pass at most one of symbol, symbols or symbol_status; combinations are not allowed, and with no "
            "parameters the rules for all symbols are returned. Request weight is 2 for symbol, 2 per symbol "
            "capped at 40 for symbols, and 40 for symbol_status or no parameters."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_execution_rules(
        symbol: str | None = Field(default=None, description="Query for a specified symbol, e.g. BTCUSDT. Optional."),
        symbols: list[str] | None = Field(
            default=None, description='Query for multiple symbols, e.g. ["BTCUSDT", "BNBUSDT"]. Optional.'
        ),
        symbol_status: str | None = Field(
            default=None,
            description="Query for all symbols with this status: TRADING, HALT, BREAK or CANCEL_ONLY. Optional.",
        ),
    ) -> SpotExecutionRulesResult:
        tlog = ToolLogger(logger, "get_spot_execution_rules")

        if symbol_status is not None and symbol_status not in _SYMBOL_STATUSES:
            return _err(
                SpotExecutionRulesResult, tlog, "VALIDATION_ERROR",
                f"symbol_status must be one of {', '.join(_SYMBOL_STATUSES)}", 400,
            )
        if sum(1 for v in (symbol, symbols, symbol_status) if v) > 1:
            return _err(
                SpotExecutionRulesResult, tlog, "VALIDATION_ERROR",
                "Provide at most one of symbol, symbols or symbol_status", 400,
            )

        try:
            data = service.call(
                "spot", "/api/v3/executionRules", "NONE", "execution_rules",
                symbol=symbol or None,
                symbols=symbols or None,
                symbol_status=symbol_status,
            )
            tlog.success()
            return SpotExecutionRulesResult(success=True, statusCode=200, data=SpotExecutionRulesData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotExecutionRulesResult, tlog, exc)

    @mcp.tool(
        name="get_spot_server_time",
        description="Returns the current Binance Spot server time in milliseconds since the Unix epoch.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_server_time() -> SpotServerTimeResult:
        tlog = ToolLogger(logger, "get_spot_server_time")

        try:
            data = service.call("spot", "/api/v3/time", "NONE", "time")
            tlog.success()
            return SpotServerTimeResult(success=True, statusCode=200, data=SpotServerTimeData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotServerTimeResult, tlog, exc)

    @mcp.tool(
        name="ping_spot",
        description="Tests connectivity to the Binance Spot REST API and returns an empty data object on success.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def ping_spot() -> PingSpotResult:
        tlog = ToolLogger(logger, "ping_spot")

        try:
            service.call("spot", "/api/v3/ping", "NONE", "ping")
            tlog.success()
            return PingSpotResult(success=True, statusCode=200, data=PingSpotData())
        except Exception as exc:
            return _handle_request_exc(PingSpotResult, tlog, exc)
