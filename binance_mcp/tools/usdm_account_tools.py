"""Usdm Account group: get_usdm_account_config, get_usdm_account, get_usdm_adl_quantile, get_usdm_algo_order, get_usdm_api_trading_status, get_usdm_bnb_burn_status, get_usdm_commission_rate, get_usdm_multi_assets_mode, get_usdm_open_order, get_usdm_order, get_usdm_order_rate_limit, get_usdm_position_mode, list_usdm_all_algo_orders, list_usdm_all_orders, list_usdm_balances, list_usdm_force_orders, list_usdm_income_history, list_usdm_leverage_brackets, list_usdm_open_algo_orders, list_usdm_open_orders, list_usdm_order_amendments, list_usdm_positions, list_usdm_symbol_config, list_usdm_user_trades"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.usdm_account import (
    UsdmAccountConfigData, UsdmAccountConfigResult,
    UsdmAccountData, UsdmAccountResult,
    UsdmAdlQuantileData, UsdmAdlQuantileResult,
    UsdmAlgoOrderData, UsdmAlgoOrderResult,
    UsdmAllAlgoOrdersListData, UsdmAllAlgoOrdersListResult,
    UsdmAllOrdersListData, UsdmAllOrdersListResult,
    UsdmApiTradingStatusData, UsdmApiTradingStatusResult,
    UsdmBalancesListData, UsdmBalancesListResult,
    UsdmBnbBurnStatusData, UsdmBnbBurnStatusResult,
    UsdmCommissionRateData, UsdmCommissionRateResult,
    UsdmForceOrdersListData, UsdmForceOrdersListResult,
    UsdmIncomeHistoryListData, UsdmIncomeHistoryListResult,
    UsdmLeverageBracketsListData, UsdmLeverageBracketsListResult,
    UsdmMultiAssetsModeData, UsdmMultiAssetsModeResult,
    UsdmOpenAlgoOrdersListData, UsdmOpenAlgoOrdersListResult,
    UsdmOpenOrderData, UsdmOpenOrderResult,
    UsdmOpenOrdersListData, UsdmOpenOrdersListResult,
    UsdmOrderAmendmentsListData, UsdmOrderAmendmentsListResult,
    UsdmOrderData, UsdmOrderResult,
    UsdmOrderRateLimitData, UsdmOrderRateLimitResult,
    UsdmPositionModeData, UsdmPositionModeResult,
    UsdmPositionsListData, UsdmPositionsListResult,
    UsdmSymbolConfigListData, UsdmSymbolConfigListResult,
    UsdmUserTradesListData, UsdmUserTradesListResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("binance-mcp.tools.usdm_account")

_ANN = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True)
_AUTH = " Reads the connected Binance account and needs an API key with read permission."
_RW = "Request validity window in milliseconds (maximum 60000). Omit to use the exchange default."
_RW_PLAIN = "Request validity window in milliseconds. Omit to use the exchange default."
_SYMBOL_OPT = "Symbol, e.g. BTCUSDT. Omit to cover all symbols."
_ORDER_ID_ONE = "Order ID. Either this or orig_client_order_id is required."
_CLIENT_ID_ONE = "Client order ID. Either this or order_id is required."

_INCOME_TYPES = [
    "TRANSFER", "WELCOME_BONUS", "REALIZED_PNL", "FUNDING_FEE", "COMMISSION", "INSURANCE_CLEAR",
    "REFERRAL_KICKBACK", "COMMISSION_REBATE", "API_REBATE", "CONTEST_REWARD",
    "CROSS_COLLATERAL_TRANSFER", "OPTIONS_PREMIUM_FEE", "OPTIONS_SETTLE_PROFIT", "INTERNAL_TRANSFER",
    "AUTO_EXCHANGE", "DELIVERED_SETTELMENT", "COIN_SWAP_DEPOSIT", "COIN_SWAP_WITHDRAW",
    "POSITION_LIMIT_INCREASE_FEE", "STRATEGY_UMFUTURES_TRANSFER", "FEE_RETURN", "BFUSD_REWARD",
    "SPECIAL_FUNDING_FEE",
]


def _rw_msg(recv_window: int | None) -> str | None:
    if recv_window is not None and recv_window > 60000:
        return "recv_window must be at most 60000"
    return None


def _limit_msg(limit: int | None, maximum: int) -> str | None:
    if limit is not None and limit > maximum:
        return f"limit must be at most {maximum}"
    return None


def register_usdm_account_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_usdm_account_config",
        description=(
            "Returns the USD-M Futures account configuration: fee tier, trading, deposit and withdraw "
            "permissions, position mode (dualSidePosition) and the multi-assets margin flag." + _AUTH
        ),
        annotations=_ANN,
    )
    def get_usdm_account_config(
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmAccountConfigResult:
        tlog = ToolLogger(logger, "get_usdm_account_config")
        if msg := _rw_msg(recv_window):
            return _err(UsdmAccountConfigResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/accountConfig", "USER_DATA", "futures_account_configuration",
                                recv_window=recv_window)
            tlog.success()
            return UsdmAccountConfigResult(success=True, statusCode=200, data=UsdmAccountConfigData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmAccountConfigResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_account",
        description=(
            "Returns the current USD-M Futures account information (V3): total margin and balance figures "
            "plus per-asset details and positions for every symbol with a position or open orders. "
            "Values are USDT-only in single-asset mode and USD-denominated in multi-assets mode." + _AUTH
        ),
        annotations=_ANN,
    )
    def get_usdm_account(
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmAccountResult:
        tlog = ToolLogger(logger, "get_usdm_account")
        if msg := _rw_msg(recv_window):
            return _err(UsdmAccountResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v3/account", "USER_DATA", "account_information_v3",
                                recv_window=recv_window)
            tlog.success()
            return UsdmAccountResult(success=True, statusCode=200, data=UsdmAccountData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmAccountResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_adl_quantile",
        description=(
            "Returns the position ADL quantile estimation per symbol, optionally for one symbol; values "
            "0 to 4 show the ADL queue position and possibility from low to high and update every 30 seconds. "
            "LONG, SHORT and BOTH are returned for one-way or isolated hedge-mode positions; for cross-margined "
            "hedge-mode positions HEDGE is returned as a sign instead of BOTH." + _AUTH
        ),
        annotations=_ANN,
    )
    def get_usdm_adl_quantile(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSDT. Omit to return all symbols."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmAdlQuantileResult:
        tlog = ToolLogger(logger, "get_usdm_adl_quantile")
        if msg := _rw_msg(recv_window):
            return _err(UsdmAdlQuantileResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/adlQuantile", "USER_DATA", "position_adl_quantile_estimation",
                                symbol=symbol, recv_window=recv_window)
            tlog.success()
            return UsdmAdlQuantileResult(success=True, statusCode=200,
                                         data=UsdmAdlQuantileData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmAdlQuantileResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_algo_order",
        description=(
            "Returns the status and details of one algo (conditional) order such as TP/SL or trailing stop; "
            "either algo_id or client_algo_id is required. Orders are not found when CANCELED or EXPIRED "
            "with no fills and created more than 3 days ago, or created more than 90 days ago." + _AUTH
        ),
        annotations=_ANN,
    )
    def get_usdm_algo_order(
        algo_id: int | None = Field(default=None, description="Algo order ID. Either this or client_algo_id is required."),
        client_algo_id: str | None = Field(default=None, description="Client algo order ID. Either this or algo_id is required."),
        recv_window: int | None = Field(default=None, description=_RW_PLAIN),
    ) -> UsdmAlgoOrderResult:
        tlog = ToolLogger(logger, "get_usdm_algo_order")
        if algo_id is None and not client_algo_id:
            return _err(UsdmAlgoOrderResult, tlog, "VALIDATION_ERROR",
                        "Either algo_id or client_algo_id is required", 400)
        try:
            data = service.call("usdm", "/fapi/v1/algoOrder", "USER_DATA", "query_algo_order",
                                algo_id=algo_id, client_algo_id=client_algo_id, recv_window=recv_window)
            tlog.success()
            return UsdmAlgoOrderResult(success=True, statusCode=200, data=UsdmAlgoOrderData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmAlgoOrderResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_api_trading_status",
        description=(
            "Returns the trading quantitative-rules indicators (lock state, planned recovery time, value and "
            "trigger threshold) per symbol and for the ACCOUNT. Request weight is 1 with a symbol and 10 "
            "when symbol is omitted." + _AUTH
        ),
        annotations=_ANN,
    )
    def get_usdm_api_trading_status(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSDT. Omit to return all symbols."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmApiTradingStatusResult:
        tlog = ToolLogger(logger, "get_usdm_api_trading_status")
        if msg := _rw_msg(recv_window):
            return _err(UsdmApiTradingStatusResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/apiTradingStatus", "USER_DATA",
                                "futures_trading_quantitative_rules_indicators",
                                symbol=symbol, recv_window=recv_window)
            tlog.success()
            return UsdmApiTradingStatusResult(success=True, statusCode=200, data=UsdmApiTradingStatusData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmApiTradingStatusResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_bnb_burn_status",
        description="Returns whether the BNB Fee Discount (fee burn) is on or off for the account." + _AUTH,
        annotations=_ANN,
    )
    def get_usdm_bnb_burn_status(
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmBnbBurnStatusResult:
        tlog = ToolLogger(logger, "get_usdm_bnb_burn_status")
        if msg := _rw_msg(recv_window):
            return _err(UsdmBnbBurnStatusResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/feeBurn", "USER_DATA", "get_bnb_burn_status",
                                recv_window=recv_window)
            tlog.success()
            return UsdmBnbBurnStatusResult(success=True, statusCode=200, data=UsdmBnbBurnStatusData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmBnbBurnStatusResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_commission_rate",
        description="Returns the account's maker, taker and RPI commission rates for a USD-M Futures symbol." + _AUTH,
        annotations=_ANN,
    )
    def get_usdm_commission_rate(
        symbol: str = Field(description="Symbol, e.g. BTCUSDT."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmCommissionRateResult:
        tlog = ToolLogger(logger, "get_usdm_commission_rate")
        if not symbol or not symbol.strip():
            return _err(UsdmCommissionRateResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if msg := _rw_msg(recv_window):
            return _err(UsdmCommissionRateResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/commissionRate", "USER_DATA", "user_commission_rate",
                                symbol=symbol, recv_window=recv_window)
            tlog.success()
            return UsdmCommissionRateResult(success=True, statusCode=200, data=UsdmCommissionRateData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmCommissionRateResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_multi_assets_mode",
        description=(
            "Returns whether the account is in Multi-Assets Mode or Single-Asset Mode, which applies to "
            "every symbol." + _AUTH
        ),
        annotations=_ANN,
    )
    def get_usdm_multi_assets_mode(
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmMultiAssetsModeResult:
        tlog = ToolLogger(logger, "get_usdm_multi_assets_mode")
        if msg := _rw_msg(recv_window):
            return _err(UsdmMultiAssetsModeResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/multiAssetsMargin", "USER_DATA", "get_current_multi_assets_mode",
                                recv_window=recv_window)
            tlog.success()
            return UsdmMultiAssetsModeResult(success=True, statusCode=200, data=UsdmMultiAssetsModeData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmMultiAssetsModeResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_open_order",
        description=(
            "Returns the details of one current open order on a USD-M Futures symbol; either order_id or "
            "orig_client_order_id is required. An order that has been filled or cancelled returns an "
            "\"Order does not exist\" error." + _AUTH
        ),
        annotations=_ANN,
    )
    def get_usdm_open_order(
        symbol: str = Field(description="Symbol, e.g. BTCUSDT."),
        order_id: int | None = Field(default=None, description=_ORDER_ID_ONE),
        orig_client_order_id: str | None = Field(default=None, description=_CLIENT_ID_ONE),
        recv_window: int | None = Field(default=None, description=_RW_PLAIN),
    ) -> UsdmOpenOrderResult:
        tlog = ToolLogger(logger, "get_usdm_open_order")
        if not symbol or not symbol.strip():
            return _err(UsdmOpenOrderResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if order_id is None and not orig_client_order_id:
            return _err(UsdmOpenOrderResult, tlog, "VALIDATION_ERROR",
                        "Either order_id or orig_client_order_id is required", 400)
        try:
            data = service.call("usdm", "/fapi/v1/openOrder", "USER_DATA", "query_current_open_order",
                                symbol=symbol, order_id=order_id, orig_client_order_id=orig_client_order_id,
                                recv_window=recv_window)
            tlog.success()
            return UsdmOpenOrderResult(success=True, statusCode=200, data=UsdmOpenOrderData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmOpenOrderResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_order",
        description=(
            "Returns the status and details of one USD-M Futures order; either order_id or "
            "orig_client_order_id is required. Orders are not found when CANCELED or EXPIRED with no fills "
            "and created more than 3 days ago, or created more than 90 days ago." + _AUTH
        ),
        annotations=_ANN,
    )
    def get_usdm_order(
        symbol: str = Field(description="Symbol, e.g. BTCUSDT."),
        order_id: int | None = Field(default=None, description=_ORDER_ID_ONE),
        orig_client_order_id: str | None = Field(default=None, description=_CLIENT_ID_ONE),
        recv_window: int | None = Field(default=None, description=_RW_PLAIN),
    ) -> UsdmOrderResult:
        tlog = ToolLogger(logger, "get_usdm_order")
        if not symbol or not symbol.strip():
            return _err(UsdmOrderResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if order_id is None and not orig_client_order_id:
            return _err(UsdmOrderResult, tlog, "VALIDATION_ERROR",
                        "Either order_id or orig_client_order_id is required", 400)
        try:
            data = service.call("usdm", "/fapi/v1/order", "USER_DATA", "query_order",
                                symbol=symbol, order_id=order_id, orig_client_order_id=orig_client_order_id,
                                recv_window=recv_window)
            tlog.success()
            return UsdmOrderResult(success=True, statusCode=200, data=UsdmOrderData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmOrderResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_order_rate_limit",
        description="Returns the account's USD-M Futures order rate limits as a list of rate limit type, interval and limit." + _AUTH,
        annotations=_ANN,
    )
    def get_usdm_order_rate_limit(
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmOrderRateLimitResult:
        tlog = ToolLogger(logger, "get_usdm_order_rate_limit")
        if msg := _rw_msg(recv_window):
            return _err(UsdmOrderRateLimitResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/rateLimit/order", "USER_DATA", "query_user_rate_limit",
                                recv_window=recv_window)
            tlog.success()
            return UsdmOrderRateLimitResult(success=True, statusCode=200,
                                            data=UsdmOrderRateLimitData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmOrderRateLimitResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_position_mode",
        description="Returns whether the account is in Hedge Mode or One-way Mode, which applies to every symbol." + _AUTH,
        annotations=_ANN,
    )
    def get_usdm_position_mode(
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmPositionModeResult:
        tlog = ToolLogger(logger, "get_usdm_position_mode")
        if msg := _rw_msg(recv_window):
            return _err(UsdmPositionModeResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/positionSide/dual", "USER_DATA", "get_current_position_mode",
                                recv_window=recv_window)
            tlog.success()
            return UsdmPositionModeResult(success=True, statusCode=200, data=UsdmPositionModeData(**data))
        except Exception as exc:
            return _handle_request_exc(UsdmPositionModeResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_all_algo_orders",
        description=(
            "Lists algo (conditional) orders for a symbol in any state (active, CANCELED, TRIGGERED, FINISHED), "
            "including TP/SL and trailing stop orders. If algo_id is set it returns orders with ID greater than or "
            "equal to it, otherwise the most recent; the time range must be under 7 days (default the recent 7 days), "
            "and CANCELED or EXPIRED orders with no fills are not found after 3 days." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_all_algo_orders(
        symbol: str = Field(description="Symbol, e.g. BTCUSDT."),
        algo_id: int | None = Field(default=None, description="Algo order ID; returns orders with ID greater than or equal to it."),
        start_time: int | None = Field(default=None, description="Start time as a Unix timestamp in milliseconds."),
        end_time: int | None = Field(default=None, description="End time as a Unix timestamp in milliseconds."),
        limit: int = Field(default=500, description="Number of records to return (maximum 1000, default 500)."),
        recv_window: int | None = Field(default=None, description=_RW_PLAIN),
    ) -> UsdmAllAlgoOrdersListResult:
        tlog = ToolLogger(logger, "list_usdm_all_algo_orders")
        if not symbol or not symbol.strip():
            return _err(UsdmAllAlgoOrdersListResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if msg := _limit_msg(limit, 1000):
            return _err(UsdmAllAlgoOrdersListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/allAlgoOrders", "USER_DATA", "query_all_algo_orders",
                                symbol=symbol, algo_id=algo_id, start_time=start_time, end_time=end_time,
                                limit=limit, recv_window=recv_window)
            tlog.success()
            return UsdmAllAlgoOrdersListResult(success=True, statusCode=200,
                                               data=UsdmAllAlgoOrdersListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmAllAlgoOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_all_orders",
        description=(
            "Lists account orders on USD-M Futures that are active, canceled or filled. If order_id is set it "
            "returns orders with ID greater than or equal to it, otherwise the most recent; the time range must be "
            "under 7 days (default the recent 7 days), and CANCELED or EXPIRED orders with no fills are not found "
            "after 3 days or any order after 90 days." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_all_orders(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSDT."),
        order_id: int | None = Field(default=None, description="Order ID; returns orders with ID greater than or equal to it."),
        start_time: int | None = Field(default=None, description="Start time as a Unix timestamp in milliseconds."),
        end_time: int | None = Field(default=None, description="End time as a Unix timestamp in milliseconds."),
        limit: int = Field(default=500, description="Number of records to return (maximum 1000, default 500)."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmAllOrdersListResult:
        tlog = ToolLogger(logger, "list_usdm_all_orders")
        if msg := _limit_msg(limit, 1000) or _rw_msg(recv_window):
            return _err(UsdmAllOrdersListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/allOrders", "USER_DATA", "all_orders",
                                symbol=symbol, order_id=order_id, start_time=start_time, end_time=end_time,
                                limit=limit, recv_window=recv_window)
            tlog.success()
            return UsdmAllOrdersListResult(success=True, statusCode=200,
                                           data=UsdmAllOrdersListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmAllOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_balances",
        description="Lists the USD-M Futures account balance per asset (wallet, cross wallet, available and withdrawable amounts)." + _AUTH,
        annotations=_ANN,
    )
    def list_usdm_balances(
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmBalancesListResult:
        tlog = ToolLogger(logger, "list_usdm_balances")
        if msg := _rw_msg(recv_window):
            return _err(UsdmBalancesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v3/balance", "USER_DATA", "futures_account_balance_v3",
                                recv_window=recv_window)
            tlog.success()
            return UsdmBalancesListResult(success=True, statusCode=200,
                                          data=UsdmBalancesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmBalancesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_force_orders",
        description=(
            "Lists the account's liquidation and auto-deleverage (ADL) force orders on USD-M Futures. Both types "
            "are returned when auto_close_type is omitted, and when start_time is omitted only data within 7 days "
            "before end_time can be queried. Request weight is 20 with a symbol and 50 without." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_force_orders(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSDT. Omit to cover all symbols."),
        auto_close_type: str | None = Field(default=None, description="LIQUIDATION for liquidation orders or ADL for ADL orders. Omit to return both."),
        start_time: int | None = Field(default=None, description="Start time as a Unix timestamp in milliseconds."),
        end_time: int | None = Field(default=None, description="End time as a Unix timestamp in milliseconds."),
        limit: int = Field(default=50, description="Number of records to return (maximum 100, default 50)."),
        recv_window: int | None = Field(default=None, description=_RW_PLAIN),
    ) -> UsdmForceOrdersListResult:
        tlog = ToolLogger(logger, "list_usdm_force_orders")
        if auto_close_type is not None and auto_close_type not in ("LIQUIDATION", "ADL"):
            return _err(UsdmForceOrdersListResult, tlog, "VALIDATION_ERROR",
                        "auto_close_type must be LIQUIDATION or ADL", 400)
        if msg := _limit_msg(limit, 100):
            return _err(UsdmForceOrdersListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/forceOrders", "USER_DATA", "users_force_orders",
                                symbol=symbol, auto_close_type=auto_close_type, start_time=start_time,
                                end_time=end_time, limit=limit, recv_window=recv_window)
            tlog.success()
            return UsdmForceOrdersListResult(success=True, statusCode=200,
                                             data=UsdmForceOrdersListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmForceOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_income_history",
        description=(
            "Lists USD-M Futures income records (transfers, realized PnL, funding fees, commissions and similar). "
            "All income types are returned when income_type is omitted, the recent 7 days are returned when "
            "start_time and end_time are omitted, and only the last three months of history is available." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_income_history(
        symbol: str | None = Field(default=None, description="Trading symbol, e.g. BTCUSDT. Omit to cover all symbols."),
        income_type: str | None = Field(default=None, description="Income type, one of: " + ", ".join(_INCOME_TYPES) + ". Omit to return all types."),
        start_time: int | None = Field(default=None, description="Start time as a Unix timestamp in milliseconds (inclusive)."),
        end_time: int | None = Field(default=None, description="End time as a Unix timestamp in milliseconds (inclusive)."),
        limit: int = Field(default=100, description="Maximum number of records to return (maximum 1000, default 100)."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmIncomeHistoryListResult:
        tlog = ToolLogger(logger, "list_usdm_income_history")
        if income_type is not None and income_type not in _INCOME_TYPES:
            return _err(UsdmIncomeHistoryListResult, tlog, "VALIDATION_ERROR",
                        "income_type must be one of: " + ", ".join(_INCOME_TYPES), 400)
        if msg := _limit_msg(limit, 1000) or _rw_msg(recv_window):
            return _err(UsdmIncomeHistoryListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/income", "USER_DATA", "get_income_history",
                                symbol=symbol, income_type=income_type, start_time=start_time,
                                end_time=end_time, limit=limit, recv_window=recv_window)
            tlog.success()
            return UsdmIncomeHistoryListResult(success=True, statusCode=200,
                                               data=UsdmIncomeHistoryListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmIncomeHistoryListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_leverage_brackets",
        description=(
            "Lists the account's notional and leverage brackets (max initial leverage, notional floor and cap, "
            "maintenance margin ratio) for all USD-M symbols, or for one symbol when symbol is given." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_leverage_brackets(
        symbol: str | None = Field(default=None, description="Symbol, e.g. ETHUSDT. Omit to return all symbols."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmLeverageBracketsListResult:
        tlog = ToolLogger(logger, "list_usdm_leverage_brackets")
        if msg := _rw_msg(recv_window):
            return _err(UsdmLeverageBracketsListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            d = service.call("usdm", "/fapi/v1/leverageBracket", "USER_DATA", "notional_and_leverage_brackets",
                             symbol=symbol, recv_window=recv_window)
            tlog.success()
            out = UsdmLeverageBracketsListData(count=len(d), items=d) if isinstance(d, list) else UsdmLeverageBracketsListData(**d)
            return UsdmLeverageBracketsListResult(success=True, statusCode=200, data=out)
        except Exception as exc:
            return _handle_request_exc(UsdmLeverageBracketsListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_open_algo_orders",
        description=(
            "Lists open algo (conditional) orders on USD-M Futures, including TP/SL and trailing stop orders, "
            "optionally filtered by algo type, symbol or algo ID. Orders for all symbols are returned when symbol "
            "is omitted, which costs request weight 40 instead of 1." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_open_algo_orders(
        algo_type: str | None = Field(default=None, description="Algo order type, e.g. CONDITIONAL. Omit to return all types."),
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSDT. Omit to return orders for all symbols."),
        algo_id: int | None = Field(default=None, description="Algo order ID."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmOpenAlgoOrdersListResult:
        tlog = ToolLogger(logger, "list_usdm_open_algo_orders")
        if msg := _rw_msg(recv_window):
            return _err(UsdmOpenAlgoOrdersListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/openAlgoOrders", "USER_DATA", "current_all_algo_open_orders",
                                algo_type=algo_type, symbol=symbol, algo_id=algo_id, recv_window=recv_window)
            tlog.success()
            return UsdmOpenAlgoOrdersListResult(success=True, statusCode=200,
                                                data=UsdmOpenAlgoOrdersListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmOpenAlgoOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_open_orders",
        description=(
            "Lists open orders on USD-M Futures for one symbol, or for all symbols when symbol is omitted, which "
            "costs request weight 40 instead of 1." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_open_orders(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSDT. Omit to return orders for all symbols."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmOpenOrdersListResult:
        tlog = ToolLogger(logger, "list_usdm_open_orders")
        if msg := _rw_msg(recv_window):
            return _err(UsdmOpenOrdersListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/openOrders", "USER_DATA", "current_all_open_orders",
                                symbol=symbol, recv_window=recv_window)
            tlog.success()
            return UsdmOpenOrdersListResult(success=True, statusCode=200,
                                            data=UsdmOpenOrdersListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmOpenOrdersListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_order_amendments",
        description=(
            "Lists the modification history of a USD-M Futures order as amendments with before and after price "
            "and quantity; either order_id or orig_client_order_id is required, and order_id is used if both are "
            "sent. History older than 3 months is not available." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_order_amendments(
        symbol: str = Field(description="Symbol, e.g. BTCUSDT."),
        order_id: int | None = Field(default=None, description=_ORDER_ID_ONE + " Takes precedence if both are sent."),
        orig_client_order_id: str | None = Field(default=None, description="Original client order ID. Either this or order_id is required."),
        start_time: int | None = Field(default=None, description="Start of the history as a Unix timestamp in milliseconds (inclusive)."),
        end_time: int | None = Field(default=None, description="End of the history as a Unix timestamp in milliseconds (inclusive)."),
        limit: int = Field(default=50, description="Number of records to return (maximum 100, default 50)."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmOrderAmendmentsListResult:
        tlog = ToolLogger(logger, "list_usdm_order_amendments")
        if not symbol or not symbol.strip():
            return _err(UsdmOrderAmendmentsListResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if order_id is None and not orig_client_order_id:
            return _err(UsdmOrderAmendmentsListResult, tlog, "VALIDATION_ERROR",
                        "Either order_id or orig_client_order_id is required", 400)
        if msg := _limit_msg(limit, 100) or _rw_msg(recv_window):
            return _err(UsdmOrderAmendmentsListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/orderAmendment", "USER_DATA", "get_order_modify_history",
                                symbol=symbol, order_id=order_id, orig_client_order_id=orig_client_order_id,
                                start_time=start_time, end_time=end_time, limit=limit, recv_window=recv_window)
            tlog.success()
            return UsdmOrderAmendmentsListResult(success=True, statusCode=200,
                                                 data=UsdmOrderAmendmentsListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmOrderAmendmentsListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_positions",
        description=(
            "Lists current USD-M Futures position information (V3); only symbols with a position or open orders "
            "are returned. Binance advises using it together with the ACCOUNT_UPDATE user data stream for "
            "timeliness and accuracy." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_positions(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSDT. Omit to return all symbols with a position or open orders."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmPositionsListResult:
        tlog = ToolLogger(logger, "list_usdm_positions")
        if msg := _rw_msg(recv_window):
            return _err(UsdmPositionsListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v3/positionRisk", "USER_DATA", "position_information_v3",
                                symbol=symbol, recv_window=recv_window)
            tlog.success()
            return UsdmPositionsListResult(success=True, statusCode=200,
                                           data=UsdmPositionsListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmPositionsListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_symbol_config",
        description="Lists the account's per-symbol configuration on USD-M Futures: margin type, auto add margin, leverage and max notional value." + _AUTH,
        annotations=_ANN,
    )
    def list_usdm_symbol_config(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSDT. Omit to return all symbols."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmSymbolConfigListResult:
        tlog = ToolLogger(logger, "list_usdm_symbol_config")
        if msg := _rw_msg(recv_window):
            return _err(UsdmSymbolConfigListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/symbolConfig", "USER_DATA", "symbol_configuration",
                                symbol=symbol, recv_window=recv_window)
            tlog.success()
            return UsdmSymbolConfigListResult(success=True, statusCode=200,
                                              data=UsdmSymbolConfigListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmSymbolConfigListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_user_trades",
        description=(
            "Lists the account's trades for one USD-M Futures symbol. The last 7 days are returned when start_time "
            "and end_time are omitted, the span between them cannot exceed 7 days, from_id cannot be combined with "
            "start_time or end_time, and only the past 3 months can be queried." + _AUTH
        ),
        annotations=_ANN,
    )
    def list_usdm_user_trades(
        symbol: str = Field(description="Symbol, e.g. BTCUSDT."),
        order_id: int | None = Field(default=None, description="Order ID to filter trades by; used together with symbol."),
        start_time: int | None = Field(default=None, description="Start time as a Unix timestamp in milliseconds."),
        end_time: int | None = Field(default=None, description="End time as a Unix timestamp in milliseconds."),
        from_id: int | None = Field(default=None, description="Trade ID to fetch from. Omit to get the most recent trades. Cannot be combined with start_time or end_time."),
        limit: int = Field(default=500, description="Number of records to return (maximum 1000, default 500)."),
        recv_window: int | None = Field(default=None, description=_RW),
    ) -> UsdmUserTradesListResult:
        tlog = ToolLogger(logger, "list_usdm_user_trades")
        if not symbol or not symbol.strip():
            return _err(UsdmUserTradesListResult, tlog, "VALIDATION_ERROR", "symbol is required", 400)
        if from_id is not None and (start_time is not None or end_time is not None):
            return _err(UsdmUserTradesListResult, tlog, "VALIDATION_ERROR",
                        "from_id cannot be sent with start_time or end_time", 400)
        if msg := _limit_msg(limit, 1000) or _rw_msg(recv_window):
            return _err(UsdmUserTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("usdm", "/fapi/v1/userTrades", "USER_DATA", "account_trade_list",
                                symbol=symbol, order_id=order_id, start_time=start_time, end_time=end_time,
                                from_id=from_id, limit=limit, recv_window=recv_window)
            tlog.success()
            return UsdmUserTradesListResult(success=True, statusCode=200,
                                            data=UsdmUserTradesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(UsdmUserTradesListResult, tlog, exc)
