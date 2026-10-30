"""Spot account group: get_spot_account, get_spot_commission_rates, get_spot_my_filters, get_spot_order_count_usage, get_spot_order_list, get_spot_order, list_spot_allocations, list_spot_all_order_lists, list_spot_all_orders, list_spot_my_trades, list_spot_open_order_lists, list_spot_open_orders, list_spot_order_amendments, list_spot_prevented_matches"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.spot_account import (
    SpotAccountData,
    SpotAccountResult,
    SpotAllocationsListData,
    SpotAllocationsListResult,
    SpotAllOrderListsListData,
    SpotAllOrderListsListResult,
    SpotAllOrdersListData,
    SpotAllOrdersListResult,
    SpotCommissionRatesData,
    SpotCommissionRatesResult,
    SpotMyFiltersData,
    SpotMyFiltersResult,
    SpotMyTradesListData,
    SpotMyTradesListResult,
    SpotOpenOrderListsListData,
    SpotOpenOrderListsListResult,
    SpotOpenOrdersListData,
    SpotOpenOrdersListResult,
    SpotOrderAmendmentsListData,
    SpotOrderAmendmentsListResult,
    SpotOrderCountUsageData,
    SpotOrderCountUsageResult,
    SpotOrderData,
    SpotOrderListData,
    SpotOrderListResult,
    SpotOrderResult,
    SpotPreventedMatchesListData,
    SpotPreventedMatchesListResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("binance-mcp.tools.spot_account")

_ANN = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True)
_AUTH = "Reads the connected Binance account and needs an API key with read permission."

_RECV_WINDOW = (
    "Request validity window in milliseconds, up to 60000; supports up to three decimal "
    "places of precision (e.g. 6000.346). Optional."
)
_LIMIT = "Maximum number of entries to return, up to 1000. Optional, defaults to 500."
_START_TIME = "Start of the time range as a Unix timestamp in milliseconds. Optional."
_END_TIME = "End of the time range as a Unix timestamp in milliseconds. Optional."

_MAX_LIMIT = 1000
_MAX_RECV_WINDOW = 60000


def _check_recv_window(recv_window: float | None) -> str | None:
    if recv_window is not None and recv_window > _MAX_RECV_WINDOW:
        return f"recv_window must be at most {_MAX_RECV_WINDOW}"
    return None


def _check_limit(limit: int) -> str | None:
    if limit > _MAX_LIMIT:
        return f"limit must be at most {_MAX_LIMIT}"
    return None


def register_spot_account_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_spot_account",
        description=(
            "Get the connected Spot account's balances, commission rates, permissions and account "
            "flags (canTrade, canWithdraw, canDeposit). Set omit_zero_balances to return only "
            "non-zero balances. " + _AUTH
        ),
        annotations=_ANN,
    )
    def get_spot_account(
        omit_zero_balances: bool = Field(
            default=False,
            description="When true, returns only the non-zero balances of the account. Optional, defaults to false.",
        ),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotAccountResult:
        tlog = ToolLogger(logger, "get_spot_account")

        if (msg := _check_recv_window(recv_window)):
            return _err(SpotAccountResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/account", "USER_DATA", "get_account",
                omit_zero_balances=omit_zero_balances, recv_window=recv_window,
            )
            tlog.success()
            return SpotAccountResult(success=True, statusCode=200, data=SpotAccountData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotAccountResult, tlog, exc)

    @mcp.tool(
        name="get_spot_commission_rates",
        description=(
            "Get the connected account's commission rates for a symbol: standard, special and tax "
            "commission plus the BNB discount settings. " + _AUTH
        ),
        annotations=_ANN,
    )
    def get_spot_commission_rates(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
    ) -> SpotCommissionRatesResult:
        tlog = ToolLogger(logger, "get_spot_commission_rates")

        if not symbol or not symbol.strip():
            return _err(SpotCommissionRatesResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)

        try:
            data = service.call(
                "spot", "/api/v3/account/commission", "USER_DATA", "account_commission",
                symbol=symbol,
            )
            tlog.success()
            return SpotCommissionRatesResult(success=True, statusCode=200, data=SpotCommissionRatesData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotCommissionRatesResult, tlog, exc)

    @mcp.tool(
        name="get_spot_my_filters",
        description=(
            "Retrieve the exchange filters, symbol filters, asset filters and rate limits that apply "
            "to the connected account on a symbol; this is the only endpoint that shows whether "
            "MAX_ASSET filters apply to the account. Each filter item carries a filterType plus keys "
            "specific to that type. " + _AUTH
        ),
        annotations=_ANN,
    )
    def get_spot_my_filters(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotMyFiltersResult:
        tlog = ToolLogger(logger, "get_spot_my_filters")

        if not symbol or not symbol.strip():
            return _err(SpotMyFiltersResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if (msg := _check_recv_window(recv_window)):
            return _err(SpotMyFiltersResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/myFilters", "USER_DATA", "my_filters",
                symbol=symbol, recv_window=recv_window,
            )
            tlog.success()
            return SpotMyFiltersResult(success=True, statusCode=200, data=SpotMyFiltersData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotMyFiltersResult, tlog, exc)

    @mcp.tool(
        name="get_spot_order_count_usage",
        description=(
            "Get the connected account's unfilled order count for each order rate-limit interval, "
            "returning the rate limit type, interval, limit and current count. " + _AUTH
        ),
        annotations=_ANN,
    )
    def get_spot_order_count_usage(
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotOrderCountUsageResult:
        tlog = ToolLogger(logger, "get_spot_order_count_usage")

        if (msg := _check_recv_window(recv_window)):
            return _err(SpotOrderCountUsageResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/rateLimit/order", "USER_DATA", "rate_limit_order",
                recv_window=recv_window,
            )
            tlog.success()
            return SpotOrderCountUsageResult(
                success=True, statusCode=200,
                data=SpotOrderCountUsageData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotOrderCountUsageResult, tlog, exc)

    @mcp.tool(
        name="get_spot_order_list",
        description=(
            "Retrieve one order list by order_list_id or by its client order ID (orig_client_order_id), "
            "returning its status and member orders. One of order_list_id or orig_client_order_id "
            "must be provided. " + _AUTH
        ),
        annotations=_ANN,
    )
    def get_spot_order_list(
        order_list_id: int | None = Field(
            default=None,
            description="Order list ID to look up. Optional, but order_list_id or orig_client_order_id must be provided.",
        ),
        orig_client_order_id: str | None = Field(
            default=None,
            description="Client order ID of the order list (listClientOrderId) to look up. Optional, but order_list_id or orig_client_order_id must be provided.",
        ),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotOrderListResult:
        tlog = ToolLogger(logger, "get_spot_order_list")

        if order_list_id is None and not orig_client_order_id:
            return _err(
                SpotOrderListResult, tlog, "VALIDATION_ERROR",
                "order_list_id or orig_client_order_id must be provided", 400,
            )
        if (msg := _check_recv_window(recv_window)):
            return _err(SpotOrderListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/orderList", "USER_DATA", "get_order_list",
                order_list_id=order_list_id, orig_client_order_id=orig_client_order_id or None,
                recv_window=recv_window,
            )
            tlog.success()
            return SpotOrderListResult(success=True, statusCode=200, data=SpotOrderListData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotOrderListResult, tlog, exc)

    @mcp.tool(
        name="get_spot_order",
        description=(
            "Check the status and details of one order on a symbol, looked up by order_id or "
            "orig_client_order_id; one of the two must be provided. If both are given, order_id is "
            "searched first and the client order ID is checked against that order, otherwise the "
            "request is rejected. A cummulativeQuoteQty below zero on some historical orders means "
            "that data is not available. " + _AUTH
        ),
        annotations=_ANN,
    )
    def get_spot_order(
        symbol: str = Field(description="Trading pair symbol, e.g. LTCBTC."),
        order_id: int | None = Field(
            default=None,
            description="Order ID to look up. Optional, but order_id or orig_client_order_id must be provided.",
        ),
        orig_client_order_id: str | None = Field(
            default=None,
            description="Client order ID of the order to look up. Optional, but order_id or orig_client_order_id must be provided.",
        ),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotOrderResult:
        tlog = ToolLogger(logger, "get_spot_order")

        if not symbol or not symbol.strip():
            return _err(SpotOrderResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if order_id is None and not orig_client_order_id:
            return _err(
                SpotOrderResult, tlog, "VALIDATION_ERROR",
                "order_id or orig_client_order_id must be provided", 400,
            )
        if (msg := _check_recv_window(recv_window)):
            return _err(SpotOrderResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/order", "USER_DATA", "get_order",
                symbol=symbol, order_id=order_id,
                orig_client_order_id=orig_client_order_id or None, recv_window=recv_window,
            )
            tlog.success()
            return SpotOrderResult(success=True, statusCode=200, data=SpotOrderData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotOrderResult, tlog, exc)

    @mcp.tool(
        name="list_spot_allocations",
        description=(
            "Retrieve the allocations resulting from SOR order placement for a symbol. The time "
            "between start_time and end_time can't exceed 24 hours; supported filters are start_time "
            "and/or end_time, from_allocation_id, or order_id (optionally with from_allocation_id). "
            + _AUTH
        ),
        annotations=_ANN,
    )
    def list_spot_allocations(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        start_time: int | None = Field(default=None, description=_START_TIME),
        end_time: int | None = Field(default=None, description=_END_TIME),
        from_allocation_id: int | None = Field(
            default=None, description="Allocation ID to start from. Optional.",
        ),
        limit: int = Field(default=500, description=_LIMIT),
        order_id: int | None = Field(
            default=None, description="Only return allocations related to this order ID. Optional.",
        ),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotAllocationsListResult:
        tlog = ToolLogger(logger, "list_spot_allocations")

        if not symbol or not symbol.strip():
            return _err(SpotAllocationsListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if (msg := _check_limit(limit) or _check_recv_window(recv_window)):
            return _err(SpotAllocationsListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/myAllocations", "USER_DATA", "my_allocations",
                symbol=symbol, start_time=start_time, end_time=end_time,
                from_allocation_id=from_allocation_id, limit=limit, order_id=order_id,
                recv_window=recv_window,
            )
            tlog.success()
            return SpotAllocationsListResult(
                success=True, statusCode=200,
                data=SpotAllocationsListData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotAllocationsListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_all_order_lists",
        description=(
            "Retrieve all of the account's order lists, filtered by the optional from_id or by a "
            "start_time/end_time range that can't exceed 24 hours. from_id can't be combined with "
            "start_time or end_time. " + _AUTH
        ),
        annotations=_ANN,
    )
    def list_spot_all_order_lists(
        from_id: int | None = Field(
            default=None,
            description="Order list ID to start from. If supplied, neither start_time nor end_time can be provided. Optional.",
        ),
        start_time: int | None = Field(default=None, description=_START_TIME),
        end_time: int | None = Field(default=None, description=_END_TIME),
        limit: int = Field(default=500, description=_LIMIT),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotAllOrderListsListResult:
        tlog = ToolLogger(logger, "list_spot_all_order_lists")

        if from_id is not None and (start_time is not None or end_time is not None):
            return _err(
                SpotAllOrderListsListResult, tlog, "VALIDATION_ERROR",
                "from_id can't be combined with start_time or end_time", 400,
            )
        if (msg := _check_limit(limit) or _check_recv_window(recv_window)):
            return _err(SpotAllOrderListsListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/allOrderList", "USER_DATA", "all_order_list",
                from_id=from_id, start_time=start_time, end_time=end_time, limit=limit,
                recv_window=recv_window,
            )
            tlog.success()
            return SpotAllOrderListsListResult(
                success=True, statusCode=200,
                data=SpotAllOrderListsListData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotAllOrderListsListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_all_orders",
        description=(
            "Get all account orders for a symbol, whether active, canceled or filled. If order_id is "
            "set, returns orders with an ID greater than or equal to it, otherwise the most recent "
            "orders; when start_time or end_time is given, order_id is not required, and the range "
            "can't exceed 24 hours. A cummulativeQuoteQty below zero on some historical orders means "
            "that data is not available. " + _AUTH
        ),
        annotations=_ANN,
    )
    def list_spot_all_orders(
        symbol: str = Field(description="Trading pair symbol, e.g. LTCBTC."),
        order_id: int | None = Field(
            default=None,
            description="If set, returns orders with an ID greater than or equal to this value; otherwise the most recent orders are returned. Optional.",
        ),
        start_time: int | None = Field(default=None, description=_START_TIME),
        end_time: int | None = Field(default=None, description=_END_TIME),
        limit: int = Field(default=500, description=_LIMIT),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotAllOrdersListResult:
        tlog = ToolLogger(logger, "list_spot_all_orders")

        if not symbol or not symbol.strip():
            return _err(SpotAllOrdersListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if (msg := _check_limit(limit) or _check_recv_window(recv_window)):
            return _err(SpotAllOrdersListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/allOrders", "USER_DATA", "all_orders",
                symbol=symbol, order_id=order_id, start_time=start_time, end_time=end_time,
                limit=limit, recv_window=recv_window,
            )
            tlog.success()
            return SpotAllOrdersListResult(
                success=True, statusCode=200,
                data=SpotAllOrdersListData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotAllOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_my_trades",
        description=(
            "Get the connected account's trades for a symbol. If from_id is set, returns trades with "
            "an ID greater than or equal to it, otherwise the most recent trades; the "
            "start_time/end_time range can't exceed 24 hours. Request weight is 20 without order_id "
            "and 5 with it. " + _AUTH
        ),
        annotations=_ANN,
    )
    def list_spot_my_trades(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBBTC."),
        order_id: int | None = Field(
            default=None,
            description="Only return trades for this order ID; can only be used in combination with symbol. Optional.",
        ),
        start_time: int | None = Field(default=None, description=_START_TIME),
        end_time: int | None = Field(default=None, description=_END_TIME),
        from_id: int | None = Field(
            default=None,
            description="Trade ID to fetch from; the most recent trades are returned if omitted. Optional.",
        ),
        limit: int = Field(default=500, description=_LIMIT),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotMyTradesListResult:
        tlog = ToolLogger(logger, "list_spot_my_trades")

        if not symbol or not symbol.strip():
            return _err(SpotMyTradesListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if (msg := _check_limit(limit) or _check_recv_window(recv_window)):
            return _err(SpotMyTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/myTrades", "USER_DATA", "my_trades",
                symbol=symbol, order_id=order_id, start_time=start_time, end_time=end_time,
                from_id=from_id, limit=limit, recv_window=recv_window,
            )
            tlog.success()
            return SpotMyTradesListResult(
                success=True, statusCode=200,
                data=SpotMyTradesListData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotMyTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_open_order_lists",
        description="List all of the account's open order lists with their status and member orders. " + _AUTH,
        annotations=_ANN,
    )
    def list_spot_open_order_lists(
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotOpenOrderListsListResult:
        tlog = ToolLogger(logger, "list_spot_open_order_lists")

        if (msg := _check_recv_window(recv_window)):
            return _err(SpotOpenOrderListsListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/openOrderList", "USER_DATA", "open_order_list",
                recv_window=recv_window,
            )
            tlog.success()
            return SpotOpenOrderListsListResult(
                success=True, statusCode=200,
                data=SpotOpenOrderListsListData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotOpenOrderListsListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_open_orders",
        description=(
            "Get all open orders on a symbol, or on all symbols when symbol is omitted. Request "
            "weight is 6 for a single symbol and 80 when symbol is omitted, so omit it with care. "
            + _AUTH
        ),
        annotations=_ANN,
    )
    def list_spot_open_orders(
        symbol: str | None = Field(
            default=None,
            description="Trading pair symbol, e.g. LTCBTC. Optional; if omitted, open orders for all symbols are returned.",
        ),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotOpenOrdersListResult:
        tlog = ToolLogger(logger, "list_spot_open_orders")

        if (msg := _check_recv_window(recv_window)):
            return _err(SpotOpenOrdersListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/openOrders", "USER_DATA", "get_open_orders",
                symbol=symbol or None, recv_window=recv_window,
            )
            tlog.success()
            return SpotOpenOrdersListResult(
                success=True, statusCode=200,
                data=SpotOpenOrdersListData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotOpenOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_order_amendments",
        description=(
            "Query all amendments of a single order, identified by symbol and order_id, returning "
            "the original and new client order IDs and quantities for each amendment. " + _AUTH
        ),
        annotations=_ANN,
    )
    def list_spot_order_amendments(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        order_id: int = Field(description="ID of the order whose amendments to list."),
        from_execution_id: int | None = Field(
            default=None, description="Execution ID to start from. Optional.",
        ),
        limit: int = Field(default=500, description=_LIMIT),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotOrderAmendmentsListResult:
        tlog = ToolLogger(logger, "list_spot_order_amendments")

        if not symbol or not symbol.strip():
            return _err(SpotOrderAmendmentsListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if (msg := _check_limit(limit) or _check_recv_window(recv_window)):
            return _err(SpotOrderAmendmentsListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/order/amendments", "USER_DATA", "order_amendments",
                symbol=symbol, order_id=order_id, from_execution_id=from_execution_id,
                limit=limit, recv_window=recv_window,
            )
            tlog.success()
            return SpotOrderAmendmentsListResult(
                success=True, statusCode=200,
                data=SpotOrderAmendmentsListData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotOrderAmendmentsListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_prevented_matches",
        description=(
            "List the orders that were expired due to self-trade prevention (STP) on a symbol. "
            "Supported combinations are symbol with prevented_match_id, symbol with order_id, and "
            "symbol with order_id and from_prevented_match_id (limit defaults to 500). Request "
            "weight is 2 when querying by prevented_match_id and 20 when querying by order_id. "
            + _AUTH
        ),
        annotations=_ANN,
    )
    def list_spot_prevented_matches(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        prevented_match_id: int | None = Field(
            default=None, description="Prevented match ID to look up. Optional.",
        ),
        order_id: int | None = Field(
            default=None, description="Order ID to list prevented matches for. Optional.",
        ),
        from_prevented_match_id: int | None = Field(
            default=None,
            description="Prevented match ID to start from; used together with order_id. Optional.",
        ),
        limit: int = Field(default=500, description=_LIMIT),
        recv_window: float | None = Field(default=None, description=_RECV_WINDOW),
    ) -> SpotPreventedMatchesListResult:
        tlog = ToolLogger(logger, "list_spot_prevented_matches")

        if not symbol or not symbol.strip():
            return _err(SpotPreventedMatchesListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if prevented_match_id is None and order_id is None:
            return _err(
                SpotPreventedMatchesListResult, tlog, "VALIDATION_ERROR",
                "prevented_match_id or order_id must be provided", 400,
            )
        if from_prevented_match_id is not None and order_id is None:
            return _err(
                SpotPreventedMatchesListResult, tlog, "VALIDATION_ERROR",
                "from_prevented_match_id requires order_id", 400,
            )
        if (msg := _check_limit(limit) or _check_recv_window(recv_window)):
            return _err(SpotPreventedMatchesListResult, tlog, "VALIDATION_ERROR", msg, 400)

        try:
            data = service.call(
                "spot", "/api/v3/myPreventedMatches", "USER_DATA", "my_prevented_matches",
                symbol=symbol, prevented_match_id=prevented_match_id, order_id=order_id,
                from_prevented_match_id=from_prevented_match_id, limit=limit,
                recv_window=recv_window,
            )
            tlog.success()
            return SpotPreventedMatchesListResult(
                success=True, statusCode=200,
                data=SpotPreventedMatchesListData(count=len(data), items=data),
            )
        except Exception as exc:
            return _handle_request_exc(SpotPreventedMatchesListResult, tlog, exc)
