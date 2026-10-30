from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ._base import ToolResult


class _Model(BaseModel):
    model_config = ConfigDict(extra="allow")


# ---- account configuration / modes -------------------------------------------------


class UsdmAccountConfigData(_Model):
    feeTier: int | None = Field(default=None, description="Account commission tier.")
    canTrade: bool | None = None
    canDeposit: bool | None = Field(default=None, description="Whether assets can be transferred in.")
    canWithdraw: bool | None = Field(default=None, description="Whether assets can be transferred out.")
    dualSidePosition: bool | None = None
    updateTime: int | None = Field(default=None, description="Reserved property.")
    multiAssetsMargin: bool | None = None
    tradeGroupId: int | None = None


class UsdmAccountConfigResult(ToolResult):
    data: UsdmAccountConfigData | None = None


class UsdmBnbBurnStatusData(_Model):
    feeBurn: bool | None = Field(default=None, description="true: Fee Discount On; false: Fee Discount Off.")


class UsdmBnbBurnStatusResult(ToolResult):
    data: UsdmBnbBurnStatusData | None = None


class UsdmMultiAssetsModeData(_Model):
    multiAssetsMargin: bool | None = Field(default=None, description="true: Multi-Assets Mode; false: Single-Asset Mode.")


class UsdmMultiAssetsModeResult(ToolResult):
    data: UsdmMultiAssetsModeData | None = None


class UsdmPositionModeData(_Model):
    dualSidePosition: bool | None = Field(default=None, description="true: Hedge Mode; false: One-way Mode.")


class UsdmPositionModeResult(ToolResult):
    data: UsdmPositionModeData | None = None


class UsdmCommissionRateData(_Model):
    symbol: str
    makerCommissionRate: str | None = None
    takerCommissionRate: str | None = None
    rpiCommissionRate: str | None = None


class UsdmCommissionRateResult(ToolResult):
    data: UsdmCommissionRateData | None = None


class UsdmApiTradingStatusData(_Model):
    indicators: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Map keyed by symbol plus an ACCOUNT key; each value is a list of objects with isLocked, "
            "plannedRecoverTime, indicator, value and triggerValue (the quantitative-rules threshold)."
        ),
    )
    updateTime: int | None = None


class UsdmApiTradingStatusResult(ToolResult):
    data: UsdmApiTradingStatusData | None = None


class UsdmOrderRateLimitItem(_Model):
    rateLimitType: str | None = None
    interval: str | None = None
    intervalNum: int | None = None
    limit: int | None = None


class UsdmOrderRateLimitData(_Model):
    count: int
    items: list[UsdmOrderRateLimitItem]


class UsdmOrderRateLimitResult(ToolResult):
    data: UsdmOrderRateLimitData | None = None


# ---- account / balances / positions -----------------------------------------------


class UsdmAccountAsset(_Model):
    asset: str | None = None
    walletBalance: str | None = None
    unrealizedProfit: str | None = None
    marginBalance: str | None = None
    maintMargin: str | None = None
    initialMargin: str | None = None
    positionInitialMargin: str | None = None
    openOrderInitialMargin: str | None = None
    crossWalletBalance: str | None = None
    crossUnPnl: str | None = None
    availableBalance: str | None = None
    maxWithdrawAmount: str | None = None
    updateTime: int | None = None


class UsdmAccountPosition(_Model):
    symbol: str | None = None
    positionSide: str | None = None
    positionAmt: str | None = None
    unrealizedProfit: str | None = None
    isolatedMargin: str | None = None
    notional: str | None = None
    isolatedWallet: str | None = None
    initialMargin: str | None = None
    maintMargin: str | None = None
    updateTime: int | None = None


class UsdmAccountData(_Model):
    totalInitialMargin: str | None = Field(default=None, description="USDT only in single-asset mode; USD-denominated in multi-assets mode.")
    totalMaintMargin: str | None = None
    totalWalletBalance: str | None = None
    totalUnrealizedProfit: str | None = None
    totalMarginBalance: str | None = None
    totalPositionInitialMargin: str | None = None
    totalOpenOrderInitialMargin: str | None = None
    totalCrossWalletBalance: str | None = None
    totalCrossUnPnl: str | None = None
    availableBalance: str | None = None
    maxWithdrawAmount: str | None = None
    assets: list[UsdmAccountAsset] | None = None
    positions: list[UsdmAccountPosition] | None = None


class UsdmAccountResult(ToolResult):
    data: UsdmAccountData | None = None


class UsdmBalance(_Model):
    asset: str | None = None
    accountAlias: str | None = Field(default=None, description="Unique account alias.")
    balance: str | None = Field(default=None, description="Wallet balance.")
    crossWalletBalance: str | None = None
    crossUnPnl: str | None = Field(default=None, description="Unrealized PnL of cross positions.")
    availableBalance: str | None = None
    maxWithdrawAmount: str | None = Field(default=None, description="Maximum transferable/withdrawable amount.")
    marginAvailable: bool | None = Field(default=None, description="Whether the asset can be used as margin in multi-assets mode.")
    updateTime: int | None = Field(default=None, description="Last update time in milliseconds.")


class UsdmBalancesListData(_Model):
    count: int
    items: list[UsdmBalance]


class UsdmBalancesListResult(ToolResult):
    data: UsdmBalancesListData | None = None


class UsdmPosition(_Model):
    symbol: str | None = None
    positionSide: str | None = None
    positionAmt: str | None = Field(default=None, description="Position amount; positive for long, negative for short.")
    entryPrice: str | None = None
    breakEvenPrice: str | None = None
    markPrice: str | None = None
    unRealizedProfit: str | None = None
    liquidationPrice: str | None = None
    isolatedMargin: str | None = None
    notional: str | None = Field(default=None, description="Notional value of the position.")
    marginAsset: str | None = None
    isolatedWallet: str | None = Field(default=None, description="Isolated wallet balance, for isolated positions.")
    initialMargin: str | None = Field(default=None, description="Initial margin required at the current mark price.")
    maintMargin: str | None = Field(default=None, description="Maintenance margin required.")
    positionInitialMargin: str | None = None
    openOrderInitialMargin: str | None = None
    adl: int | None = Field(default=None, description="Auto-deleverage ranking.")
    bidNotional: str | None = None
    askNotional: str | None = None
    updateTime: int | None = None


class UsdmPositionsListData(_Model):
    count: int
    items: list[UsdmPosition]


class UsdmPositionsListResult(ToolResult):
    data: UsdmPositionsListData | None = None


class UsdmAdlQuantileValues(_Model):
    LONG: int | None = Field(default=None, description="ADL quantile for the LONG position in hedge mode.")
    SHORT: int | None = Field(default=None, description="ADL quantile for the SHORT position in hedge mode.")
    HEDGE: int | None = Field(default=None, description="Only a sign for cross-margined hedge-mode positions; the value carries no meaning.")
    BOTH: int | None = Field(default=None, description="ADL quantile for the position in one-way mode.")


class UsdmAdlQuantileItem(_Model):
    symbol: str
    adlQuantile: UsdmAdlQuantileValues | None = Field(default=None, description="Values 0-4 show ADL possibility from low to high.")


class UsdmAdlQuantileData(_Model):
    count: int
    items: list[UsdmAdlQuantileItem]


class UsdmAdlQuantileResult(ToolResult):
    data: UsdmAdlQuantileData | None = None


class UsdmSymbolConfigItem(_Model):
    symbol: str
    marginType: str | None = None
    isAutoAddMargin: bool | None = None
    leverage: int | None = None
    maxNotionalValue: str | None = None


class UsdmSymbolConfigListData(_Model):
    count: int
    items: list[UsdmSymbolConfigItem]


class UsdmSymbolConfigListResult(ToolResult):
    data: UsdmSymbolConfigListData | None = None


class UsdmLeverageBracket(_Model):
    bracket: int | None = Field(default=None, description="Notional bracket.")
    initialLeverage: int | None = Field(default=None, description="Max initial leverage for this bracket.")
    notionalCap: float | None = Field(default=None, description="Cap notional of this bracket.")
    notionalFloor: float | None = Field(default=None, description="Notional threshold of this bracket.")
    maintMarginRatio: float | None = Field(default=None, description="Maintenance ratio for this bracket.")
    cum: float | None = Field(default=None, description="Auxiliary number for quick calculation.")


class UsdmLeverageBracketsItem(_Model):
    symbol: str | None = None
    notionalCoef: float | None = Field(default=None, description="User symbol bracket multiplier, only present when the user's symbol bracket is adjusted.")
    brackets: list[UsdmLeverageBracket] | None = None


class UsdmLeverageBracketsListData(_Model):
    count: int | None = None
    items: list[UsdmLeverageBracketsItem] | None = None
    symbol: str | None = None
    notionalCoef: float | None = Field(default=None, description="User symbol bracket multiplier, only present when the user's symbol bracket is adjusted.")
    brackets: list[UsdmLeverageBracket] | None = None


class UsdmLeverageBracketsListResult(ToolResult):
    data: UsdmLeverageBracketsListData | None = None


# ---- orders ------------------------------------------------------------------------


class UsdmOrderInfo(_Model):
    orderId: int
    symbol: str | None = None
    pair: str | None = None
    clientOrderId: str | None = None
    status: str | None = None
    type: str | None = None
    origType: str | None = None
    side: str | None = None
    positionSide: str | None = None
    timeInForce: str | None = None
    price: str | None = None
    avgPrice: str | None = None
    origQty: str | None = None
    executedQty: str | None = None
    cumQuote: str | None = None
    cumBase: str | None = None
    reduceOnly: bool | None = None
    closePosition: bool | None = Field(default=None, description="Whether the order closes the whole position (Close-All).")
    stopPrice: str | None = Field(default=None, description="Not meaningful when the order type is TRAILING_STOP_MARKET.")
    activatePrice: str | None = Field(default=None, description="Activation price, only returned for TRAILING_STOP_MARKET orders.")
    priceRate: str | None = Field(default=None, description="Callback rate, only returned for TRAILING_STOP_MARKET orders.")
    workingType: str | None = None
    priceProtect: bool | None = Field(default=None, description="Whether conditional order trigger protection is enabled.")
    priceMatch: str | None = Field(default=None, description="Price match mode.")
    selfTradePreventionMode: str | None = None
    goodTillDate: int | None = Field(default=None, description="Pre-set auto-cancel time for a TIF GTD order.")
    time: int | None = Field(default=None, description="Order time in milliseconds.")
    updateTime: int | None = None


class UsdmOrderData(UsdmOrderInfo):
    pass


class UsdmOrderResult(ToolResult):
    data: UsdmOrderData | None = None


class UsdmOpenOrderData(UsdmOrderInfo):
    pass


class UsdmOpenOrderResult(ToolResult):
    data: UsdmOpenOrderData | None = None


class UsdmAllOrdersListData(_Model):
    count: int
    items: list[UsdmOrderInfo]


class UsdmAllOrdersListResult(ToolResult):
    data: UsdmAllOrdersListData | None = None


class UsdmOpenOrdersListData(_Model):
    count: int
    items: list[UsdmOrderInfo]


class UsdmOpenOrdersListResult(ToolResult):
    data: UsdmOpenOrdersListData | None = None


class UsdmForceOrdersListData(_Model):
    count: int
    items: list[UsdmOrderInfo]


class UsdmForceOrdersListResult(ToolResult):
    data: UsdmForceOrdersListData | None = None


class UsdmAlgoOrderInfo(_Model):
    algoId: int
    clientAlgoId: str | None = None
    algoType: str | None = None
    orderType: str | None = None
    symbol: str | None = None
    side: str | None = None
    positionSide: str | None = None
    timeInForce: str | None = None
    quantity: str | None = None
    algoStatus: str | None = None
    actualOrderId: str | None = Field(default=None, description="Empty string if not triggered; the order ID if triggered.")
    actualPrice: str | None = Field(default=None, description="0 if not triggered; average price if filled or partially filled.")
    actualType: str | None = Field(default=None, description="Only present when triggered.")
    actualQty: str | None = Field(default=None, description="Only present when filled or partially filled.")
    triggerPrice: str | None = None
    price: str | None = None
    icebergQuantity: str | None = None
    tpTriggerPrice: str | None = None
    tpPrice: str | None = None
    slTriggerPrice: str | None = None
    slPrice: str | None = None
    tpOrderType: str | None = None
    selfTradePreventionMode: str | None = None
    workingType: str | None = None
    priceMatch: str | None = None
    closePosition: bool | None = None
    priceProtect: bool | None = None
    reduceOnly: bool | None = None
    createTime: int | None = None
    updateTime: int | None = None
    triggerTime: int | None = None
    goodTillDate: int | None = None


class UsdmAlgoOrderData(UsdmAlgoOrderInfo):
    pass


class UsdmAlgoOrderResult(ToolResult):
    data: UsdmAlgoOrderData | None = None


class UsdmAllAlgoOrdersListData(_Model):
    count: int
    items: list[UsdmAlgoOrderInfo]


class UsdmAllAlgoOrdersListResult(ToolResult):
    data: UsdmAllAlgoOrdersListData | None = None


class UsdmOpenAlgoOrdersListData(_Model):
    count: int
    items: list[UsdmAlgoOrderInfo]


class UsdmOpenAlgoOrdersListResult(ToolResult):
    data: UsdmOpenAlgoOrdersListData | None = None


class UsdmBeforeAfter(_Model):
    before: str | None = None
    after: str | None = None


class UsdmAmendmentDetail(_Model):
    price: UsdmBeforeAfter | None = None
    origQty: UsdmBeforeAfter | None = None
    count: int | None = Field(default=None, description="Number of times the order has been modified.")
    modifyId: int | None = Field(default=None, description="User-defined modification identifier, only returned if provided in the request.")


class UsdmOrderAmendment(_Model):
    amendmentId: int | None = Field(default=None, description="Order modification ID.")
    symbol: str | None = None
    pair: str | None = None
    orderId: int | None = None
    clientOrderId: str | None = None
    time: int | None = Field(default=None, description="Order modification time in milliseconds.")
    amendment: UsdmAmendmentDetail | None = None


class UsdmOrderAmendmentsListData(_Model):
    count: int
    items: list[UsdmOrderAmendment]


class UsdmOrderAmendmentsListResult(ToolResult):
    data: UsdmOrderAmendmentsListData | None = None


# ---- trades / income ---------------------------------------------------------------


class UsdmUserTrade(_Model):
    id: int
    symbol: str | None = None
    pair: str | None = None
    orderId: int | None = None
    side: str | None = None
    positionSide: str | None = None
    price: str | None = None
    qty: str | None = None
    quoteQty: str | None = Field(default=None, description="Quote asset quantity; populated for USD-M symbols.")
    baseQty: str | None = Field(default=None, description="Base asset quantity; \"0\" for USD-M symbols.")
    commission: str | None = None
    commissionAsset: str | None = None
    marginAsset: str | None = None
    realizedPnl: str | None = None
    buyer: bool | None = None
    maker: bool | None = None
    time: int | None = None


class UsdmUserTradesListData(_Model):
    count: int
    items: list[UsdmUserTrade]


class UsdmUserTradesListResult(ToolResult):
    data: UsdmUserTradesListData | None = None


class UsdmIncomeRecord(_Model):
    symbol: str | None = Field(default=None, description="Trade symbol, if existing.")
    incomeType: str | None = None
    income: str | None = Field(default=None, description="Income amount.")
    asset: str | None = Field(default=None, description="Income asset.")
    info: str | None = Field(default=None, description="Extra information.")
    time: int | None = None
    tranId: int | None = Field(default=None, description="Transaction ID; unique within the same incomeType.")
    tradeId: str | None = Field(default=None, description="Trade ID, if existing.")


class UsdmIncomeHistoryListData(_Model):
    count: int
    items: list[UsdmIncomeRecord]


class UsdmIncomeHistoryListResult(ToolResult):
    data: UsdmIncomeHistoryListData | None = None
