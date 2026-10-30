"""Coinm account group: get_coinm_account, get_coinm_adl_quantile, get_coinm_commission_rate, get_coinm_open_order, get_coinm_order, get_coinm_position_mode, list_coinm_all_orders, list_coinm_balances, list_coinm_force_orders, list_coinm_income_history, list_coinm_leverage_brackets, list_coinm_open_orders, list_coinm_order_amendments, list_coinm_positions, list_coinm_user_trades"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.coinm_account import (
    CoinmAccountData,
    CoinmAccountResult,
    CoinmAdlQuantileData,
    CoinmAdlQuantileResult,
    CoinmAllOrdersListData,
    CoinmAllOrdersListResult,
    CoinmBalancesListData,
    CoinmBalancesListResult,
    CoinmCommissionRateData,
    CoinmCommissionRateResult,
    CoinmForceOrdersListData,
    CoinmForceOrdersListResult,
    CoinmIncomeHistoryListData,
    CoinmIncomeHistoryListResult,
    CoinmLeverageBracketsListData,
    CoinmLeverageBracketsListResult,
    CoinmOpenOrderData,
    CoinmOpenOrderResult,
    CoinmOpenOrdersListData,
    CoinmOpenOrdersListResult,
    CoinmOrderAmendmentsListData,
    CoinmOrderAmendmentsListResult,
    CoinmOrderData,
    CoinmOrderResult,
    CoinmPositionModeData,
    CoinmPositionModeResult,
    CoinmPositionsListData,
    CoinmPositionsListResult,
    CoinmUserTradesListData,
    CoinmUserTradesListResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("binance-mcp.tools.coinm_account")

_ACCOUNT_READ = " Reads the connected Binance account and needs an API key with read permission."
_RECV_MAX = 60000
_RECV_MSG = f"recv_window must be at most {_RECV_MAX}"
_RECV_DESC = "Request validity window in milliseconds, at most 60000. Omit to use the Binance default."
_INCOME_TYPES = ["TRANSFER", "WELCOME_BONUS", "FUNDING_FEE", "REALIZED_PNL", "COMMISSION", "INSURANCE_CLEAR", "DELIVERED_SETTELMENT"]
_FORCE_TYPES = ["LIQUIDATION", "ADL"]


def _recv_bad(recv_window: int | None) -> bool:
    return recv_window is not None and recv_window > _RECV_MAX


def register_coinm_account_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_coinm_account",
        description=(
            "Gets the COIN-M Futures account overview, returning per-asset margin balances, positions, "
            "the trading, deposit and withdraw flags, and the fee tier. One-way Mode accounts see only "
            "BOTH positions; Hedge Mode accounts see BOTH, LONG and SHORT positions." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_account(
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmAccountResult:
        tlog = ToolLogger(logger, "get_coinm_account")

        if _recv_bad(recv_window):
            return _err(CoinmAccountResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call("coinm", "/dapi/v1/account", "USER_DATA", "account_information", recv_window=recv_window)
            result = CoinmAccountData(**data)
            tlog.success()
            return CoinmAccountResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmAccountResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_adl_quantile",
        description=(
            "Gets the position ADL quantile estimate, returning one entry per symbol with the quantile for each "
            "position side. Values 0 to 4 run from low to high ADL likelihood and refresh every 30 seconds; "
            "symbol is optional. Cross-margined Hedge Mode positions report HEDGE in place of BOTH." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_adl_quantile(
        symbol: str | None = Field(default=None, description="COIN-M symbol, for example BTCUSD_PERP. Omit to query without a symbol filter."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmAdlQuantileResult:
        tlog = ToolLogger(logger, "get_coinm_adl_quantile")

        if _recv_bad(recv_window):
            return _err(CoinmAdlQuantileResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/adlQuantile", "USER_DATA", "position_adl_quantile_estimation",
                symbol=symbol, recv_window=recv_window,
            )
            result = CoinmAdlQuantileData(count=len(data), items=data)
            tlog.success()
            return CoinmAdlQuantileResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmAdlQuantileResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_commission_rate",
        description="Gets the user's commission rates for a symbol, returning the maker and taker commission rates." + _ACCOUNT_READ,
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_commission_rate(
        symbol: str = Field(description="COIN-M symbol, for example BTCUSD_PERP."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmCommissionRateResult:
        tlog = ToolLogger(logger, "get_coinm_commission_rate")

        if not symbol or not symbol.strip():
            return _err(CoinmCommissionRateResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if _recv_bad(recv_window):
            return _err(CoinmCommissionRateResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/commissionRate", "USER_DATA", "user_commission_rate",
                symbol=symbol, recv_window=recv_window,
            )
            result = CoinmCommissionRateData(**data)
            tlog.success()
            return CoinmCommissionRateResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmCommissionRateResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_open_order",
        description=(
            "Gets a single current open order by order ID or client order ID, returning its status and execution "
            "details. Either order_id or orig_client_order_id is required, and an order that has been filled or "
            "cancelled returns the error \"Order does not exist\"." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_open_order(
        symbol: str = Field(description="COIN-M symbol, for example BTCUSD_PERP."),
        order_id: int | None = Field(default=None, description="Order ID. Either order_id or orig_client_order_id is required."),
        orig_client_order_id: str | None = Field(default=None, description="Client order ID. Either order_id or orig_client_order_id is required."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmOpenOrderResult:
        tlog = ToolLogger(logger, "get_coinm_open_order")

        if not symbol or not symbol.strip():
            return _err(CoinmOpenOrderResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if order_id is None and not orig_client_order_id:
            return _err(CoinmOpenOrderResult, tlog, "VALIDATION_ERROR", "Either order_id or orig_client_order_id is required", 400)
        if _recv_bad(recv_window):
            return _err(CoinmOpenOrderResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/openOrder", "USER_DATA", "query_current_open_order",
                symbol=symbol, order_id=order_id, orig_client_order_id=orig_client_order_id, recv_window=recv_window,
            )
            result = CoinmOpenOrderData(**data)
            tlog.success()
            return CoinmOpenOrderResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmOpenOrderResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_order",
        description=(
            "Gets an order's status by order ID or client order ID, returning its execution details. Either "
            "order_id or orig_client_order_id is required; a canceled or expired order with no fills is not found "
            "once it is older than 3 days, and no order is found once it is older than 90 days." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_order(
        symbol: str = Field(description="COIN-M symbol, for example BTCUSD_PERP."),
        order_id: int | None = Field(default=None, description="Order ID. Either order_id or orig_client_order_id is required."),
        orig_client_order_id: str | None = Field(default=None, description="Client order ID. Either order_id or orig_client_order_id is required."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmOrderResult:
        tlog = ToolLogger(logger, "get_coinm_order")

        if not symbol or not symbol.strip():
            return _err(CoinmOrderResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if order_id is None and not orig_client_order_id:
            return _err(CoinmOrderResult, tlog, "VALIDATION_ERROR", "Either order_id or orig_client_order_id is required", 400)
        if _recv_bad(recv_window):
            return _err(CoinmOrderResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/order", "USER_DATA", "query_order",
                symbol=symbol, order_id=order_id, orig_client_order_id=orig_client_order_id, recv_window=recv_window,
            )
            result = CoinmOrderData(**data)
            tlog.success()
            return CoinmOrderResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmOrderResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_position_mode",
        description=(
            "Gets the user's position mode, which applies to every symbol, returning dualSidePosition "
            "(true for Hedge Mode, false for One-way Mode)." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_position_mode(
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmPositionModeResult:
        tlog = ToolLogger(logger, "get_coinm_position_mode")

        if _recv_bad(recv_window):
            return _err(CoinmPositionModeResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/positionSide/dual", "USER_DATA", "get_current_position_mode", recv_window=recv_window,
            )
            result = CoinmPositionModeData(**data)
            tlog.success()
            return CoinmPositionModeResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmPositionModeResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_all_orders",
        description=(
            "Lists account orders (active, canceled or filled) for a symbol or pair, returning order records. "
            "Either symbol or pair is required and pair cannot be combined with order_id; with order_id set it "
            "returns orders from that ID onward, otherwise the most recent. The time range must be under 7 days "
            "(the last 7 days by default), and canceled or expired orders with no fills older than 3 days, or any "
            "order older than 90 days, are not returned." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_all_orders(
        symbol: str | None = Field(default=None, description="COIN-M symbol, for example BTCUSD_PERP. Either symbol or pair is required."),
        pair: str | None = Field(default=None, description="Pair, for example BTCUSD. Either symbol or pair is required; cannot be sent with order_id."),
        order_id: int | None = Field(default=None, description="Order ID. When set, returns orders with an ID greater than or equal to it; otherwise the most recent orders."),
        start_time: int | None = Field(default=None, description="Start of the time range as a Unix timestamp in milliseconds. The range must be under 7 days."),
        end_time: int | None = Field(default=None, description="End of the time range as a Unix timestamp in milliseconds. The range must be under 7 days."),
        limit: int = Field(default=50, description="Maximum number of records to return, at most 100."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmAllOrdersListResult:
        tlog = ToolLogger(logger, "list_coinm_all_orders")

        if not symbol and not pair:
            return _err(CoinmAllOrdersListResult, tlog, "VALIDATION_ERROR", "Either symbol or pair is required", 400)
        if pair and order_id is not None:
            return _err(CoinmAllOrdersListResult, tlog, "VALIDATION_ERROR", "pair cannot be sent with order_id", 400)
        if limit > 100:
            return _err(CoinmAllOrdersListResult, tlog, "VALIDATION_ERROR", "limit must be at most 100", 400)
        if _recv_bad(recv_window):
            return _err(CoinmAllOrdersListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/allOrders", "USER_DATA", "all_orders",
                symbol=symbol, pair=pair, order_id=order_id, start_time=start_time, end_time=end_time,
                limit=limit, recv_window=recv_window,
            )
            result = CoinmAllOrdersListData(count=len(data), items=data)
            tlog.success()
            return CoinmAllOrdersListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmAllOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_balances",
        description="Lists the futures account balances, returning one record per asset with balance, withdrawable amount, cross wallet balance, cross unrealized PnL and available balance." + _ACCOUNT_READ,
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_balances(
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmBalancesListResult:
        tlog = ToolLogger(logger, "list_coinm_balances")

        if _recv_bad(recv_window):
            return _err(CoinmBalancesListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call("coinm", "/dapi/v1/balance", "USER_DATA", "futures_account_balance", recv_window=recv_window)
            result = CoinmBalancesListData(count=len(data), items=data)
            tlog.success()
            return CoinmBalancesListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmBalancesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_force_orders",
        description=(
            "Lists the user's force orders (liquidation or ADL), returning order records. Omitting auto_close_type "
            "returns both types, and only the past 90 days can be queried." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_force_orders(
        symbol: str | None = Field(default=None, description="COIN-M symbol, for example BTCUSD_PERP. Omit to query without a symbol filter."),
        auto_close_type: str | None = Field(default=None, description="Force order type: LIQUIDATION or ADL. Omit to return both types."),
        start_time: int | None = Field(default=None, description="Start of the time range as a Unix timestamp in milliseconds."),
        end_time: int | None = Field(default=None, description="End of the time range as a Unix timestamp in milliseconds."),
        limit: int = Field(default=50, description="Maximum number of records to return, at most 100."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmForceOrdersListResult:
        tlog = ToolLogger(logger, "list_coinm_force_orders")

        if auto_close_type is not None and auto_close_type not in _FORCE_TYPES:
            return _err(CoinmForceOrdersListResult, tlog, "VALIDATION_ERROR", f"auto_close_type must be one of {_FORCE_TYPES}", 400)
        if limit > 100:
            return _err(CoinmForceOrdersListResult, tlog, "VALIDATION_ERROR", "limit must be at most 100", 400)
        if _recv_bad(recv_window):
            return _err(CoinmForceOrdersListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/forceOrders", "USER_DATA", "users_force_orders",
                symbol=symbol, auto_close_type=auto_close_type, start_time=start_time, end_time=end_time,
                limit=limit, recv_window=recv_window,
            )
            result = CoinmForceOrdersListData(count=len(data), items=data)
            tlog.success()
            return CoinmForceOrdersListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmForceOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_income_history",
        description=(
            "Lists income history records such as funding fees, realized PnL, commissions and transfers, returning "
            "one record per flow. Omitting income_type returns all kinds of flow, and the time between start_time "
            "and end_time cannot be longer than 1 year." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_income_history(
        symbol: str | None = Field(default=None, description="COIN-M symbol, for example BTCUSD_PERP. Omit to query without a symbol filter."),
        income_type: str | None = Field(
            default=None,
            description="Income type: TRANSFER, WELCOME_BONUS, FUNDING_FEE, REALIZED_PNL, COMMISSION, INSURANCE_CLEAR or DELIVERED_SETTELMENT. Omit to return all kinds of flow.",
        ),
        start_time: int | None = Field(default=None, description="Timestamp in milliseconds to get income from, inclusive. The range to end_time cannot exceed 1 year."),
        end_time: int | None = Field(default=None, description="Timestamp in milliseconds to get income until, inclusive. The range from start_time cannot exceed 1 year."),
        limit: int = Field(default=100, description="Maximum number of records to return, at most 1000."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmIncomeHistoryListResult:
        tlog = ToolLogger(logger, "list_coinm_income_history")

        if income_type is not None and income_type not in _INCOME_TYPES:
            return _err(CoinmIncomeHistoryListResult, tlog, "VALIDATION_ERROR", f"income_type must be one of {_INCOME_TYPES}", 400)
        if limit > 1000:
            return _err(CoinmIncomeHistoryListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1000", 400)
        if _recv_bad(recv_window):
            return _err(CoinmIncomeHistoryListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/income", "USER_DATA", "get_income_history",
                symbol=symbol, income_type=income_type, start_time=start_time, end_time=end_time,
                limit=limit, recv_window=recv_window,
            )
            result = CoinmIncomeHistoryListData(count=len(data), items=data)
            tlog.success()
            return CoinmIncomeHistoryListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmIncomeHistoryListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_leverage_brackets",
        description=(
            "Lists the notional leverage brackets per symbol, returning each bracket's maximum initial leverage, "
            "base asset quantity range and maintenance margin ratio. symbol is optional." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_leverage_brackets(
        symbol: str | None = Field(default=None, description="COIN-M symbol, for example BTCUSD_PERP. Omit to query without a symbol filter."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmLeverageBracketsListResult:
        tlog = ToolLogger(logger, "list_coinm_leverage_brackets")

        if _recv_bad(recv_window):
            return _err(CoinmLeverageBracketsListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v2/leverageBracket", "USER_DATA", "notional_bracket_for_symbol",
                symbol=symbol, recv_window=recv_window,
            )
            result = CoinmLeverageBracketsListData(count=len(data), items=data)
            tlog.success()
            return CoinmLeverageBracketsListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmLeverageBracketsListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_open_orders",
        description=(
            "Lists all current open orders on a symbol or pair, returning order records. Calling without a symbol "
            "returns open orders across all symbols and costs more request weight (40 versus 1 for a single symbol)." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_open_orders(
        symbol: str | None = Field(default=None, description="COIN-M symbol, for example BTCUSD_PERP. An invalid symbol returns error -1121. Omit to query without a symbol filter."),
        pair: str | None = Field(default=None, description="Pair, for example BTCUSD."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmOpenOrdersListResult:
        tlog = ToolLogger(logger, "list_coinm_open_orders")

        if _recv_bad(recv_window):
            return _err(CoinmOpenOrdersListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/openOrders", "USER_DATA", "current_all_open_orders",
                symbol=symbol, pair=pair, recv_window=recv_window,
            )
            result = CoinmOpenOrdersListData(count=len(data), items=data)
            tlog.success()
            return CoinmOpenOrdersListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmOpenOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_order_amendments",
        description=(
            "Lists the modification history of an order, returning amendment records with before and after price "
            "and quantity. Either order_id or orig_client_order_id is required (order_id is used when both are "
            "sent), and history older than 3 months is not available." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_order_amendments(
        symbol: str = Field(description="COIN-M symbol, for example BTCUSD_PERP."),
        order_id: int | None = Field(default=None, description="Order ID. Either order_id or orig_client_order_id is required; order_id is used when both are sent."),
        orig_client_order_id: str | None = Field(default=None, description="Client order ID. Either order_id or orig_client_order_id is required."),
        start_time: int | None = Field(default=None, description="Timestamp in milliseconds to get modification history from, inclusive."),
        end_time: int | None = Field(default=None, description="Timestamp in milliseconds to get modification history until, inclusive."),
        limit: int = Field(default=50, description="Maximum number of records to return, at most 100."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmOrderAmendmentsListResult:
        tlog = ToolLogger(logger, "list_coinm_order_amendments")

        if not symbol or not symbol.strip():
            return _err(CoinmOrderAmendmentsListResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if order_id is None and not orig_client_order_id:
            return _err(CoinmOrderAmendmentsListResult, tlog, "VALIDATION_ERROR", "Either order_id or orig_client_order_id is required", 400)
        if limit > 100:
            return _err(CoinmOrderAmendmentsListResult, tlog, "VALIDATION_ERROR", "limit must be at most 100", 400)
        if _recv_bad(recv_window):
            return _err(CoinmOrderAmendmentsListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/orderAmendment", "USER_DATA", "get_order_modify_history",
                symbol=symbol, order_id=order_id, orig_client_order_id=orig_client_order_id,
                start_time=start_time, end_time=end_time, limit=limit, recv_window=recv_window,
            )
            result = CoinmOrderAmendmentsListData(count=len(data), items=data)
            tlog.success()
            return CoinmOrderAmendmentsListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmOrderAmendmentsListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_positions",
        description=(
            "Lists current position information, returning entry, mark and liquidation prices and margin details "
            "per position. Without margin_asset and pair, positions of all symbols with TRADING status are "
            "returned; One-way Mode accounts see only BOTH positions and Hedge Mode accounts see BOTH, LONG and "
            "SHORT positions." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_positions(
        margin_asset: str | None = Field(default=None, description="Margin asset, for example BTC. Omit together with pair to return all TRADING symbols."),
        pair: str | None = Field(default=None, description="Pair, for example BTCUSD. Omit together with margin_asset to return all TRADING symbols."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmPositionsListResult:
        tlog = ToolLogger(logger, "list_coinm_positions")

        if _recv_bad(recv_window):
            return _err(CoinmPositionsListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/positionRisk", "USER_DATA", "position_information",
                margin_asset=margin_asset, pair=pair, recv_window=recv_window,
            )
            result = CoinmPositionsListData(count=len(data), items=data)
            tlog.success()
            return CoinmPositionsListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmPositionsListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_user_trades",
        description=(
            "Lists the account's trades for a symbol or pair, returning trade records with price, quantity, "
            "commission and realized PnL. Exactly one of symbol or pair is required; order_id works only with "
            "symbol, and from_id cannot be combined with pair, start_time or end_time. The time range cannot "
            "exceed 7 days (the last 7 days by default) and only the past 3 months can be queried." + _ACCOUNT_READ
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_user_trades(
        symbol: str | None = Field(default=None, description="COIN-M symbol, for example BTCUSD_PERP. Either symbol or pair is required, not both."),
        pair: str | None = Field(default=None, description="Pair, for example BTCUSD. Either symbol or pair is required, not both; returns trades for all symbols of the pair."),
        order_id: str | None = Field(default=None, description="Order ID. Can only be sent together with symbol."),
        start_time: int | None = Field(default=None, description="Start of the time range as a Unix timestamp in milliseconds. Cannot be sent with from_id; the range cannot exceed 7 days."),
        end_time: int | None = Field(default=None, description="End of the time range as a Unix timestamp in milliseconds. Cannot be sent with from_id; the range cannot exceed 7 days."),
        from_id: int | None = Field(default=None, description="Trade ID to fetch from. Omit to get the most recent trades. Cannot be sent with pair, start_time or end_time."),
        limit: int = Field(default=50, description="Maximum number of records to return, at most 1000."),
        recv_window: int | None = Field(default=None, description=_RECV_DESC),
    ) -> CoinmUserTradesListResult:
        tlog = ToolLogger(logger, "list_coinm_user_trades")

        if not symbol and not pair:
            return _err(CoinmUserTradesListResult, tlog, "VALIDATION_ERROR", "Either symbol or pair is required", 400)
        if symbol and pair:
            return _err(CoinmUserTradesListResult, tlog, "VALIDATION_ERROR", "symbol and pair cannot be sent together", 400)
        if pair and from_id is not None:
            return _err(CoinmUserTradesListResult, tlog, "VALIDATION_ERROR", "pair and from_id cannot be sent together", 400)
        if order_id is not None and not symbol:
            return _err(CoinmUserTradesListResult, tlog, "VALIDATION_ERROR", "order_id can only be sent together with symbol", 400)
        if from_id is not None and (start_time is not None or end_time is not None):
            return _err(CoinmUserTradesListResult, tlog, "VALIDATION_ERROR", "from_id cannot be sent with start_time or end_time", 400)
        if limit > 1000:
            return _err(CoinmUserTradesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1000", 400)
        if _recv_bad(recv_window):
            return _err(CoinmUserTradesListResult, tlog, "VALIDATION_ERROR", _RECV_MSG, 400)

        try:
            data = service.call(
                "coinm", "/dapi/v1/userTrades", "USER_DATA", "account_trade_list",
                symbol=symbol, pair=pair, order_id=order_id, start_time=start_time, end_time=end_time,
                from_id=from_id, limit=limit, recv_window=recv_window,
            )
            result = CoinmUserTradesListData(count=len(data), items=data)
            tlog.success()
            return CoinmUserTradesListResult(success=True, statusCode=200, data=result)
        except Exception as exc:
            return _handle_request_exc(CoinmUserTradesListResult, tlog, exc)
