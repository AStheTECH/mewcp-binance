from pydantic import BaseModel, ConfigDict, Field

from ._base import ToolResult


class AccountAsset(BaseModel):
    model_config = ConfigDict(extra="allow")

    asset: str
    walletBalance: str | None = None
    unrealizedProfit: str | None = None
    marginBalance: str | None = None
    maintMargin: str | None = None
    initialMargin: str | None = Field(default=None, description="Total initial margin required with the latest mark price.")
    positionInitialMargin: str | None = Field(default=None, description="Positions' margin required with the latest mark price.")
    openOrderInitialMargin: str | None = Field(default=None, description="Open orders' initial margin required with the latest mark price.")
    maxWithdrawAmount: str | None = Field(default=None, description="Maximum amount for transfer out.")
    crossWalletBalance: str | None = Field(default=None, description="Wallet balance for crossed margin.")
    crossUnPnl: str | None = Field(default=None, description="Total unrealized profit or loss of crossed positions.")
    availableBalance: str | None = Field(default=None, description="Available margin balance.")
    updateTime: int | None = None


class AccountPosition(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    positionAmt: str | None = None
    initialMargin: str | None = None
    maintMargin: str | None = None
    unrealizedProfit: str | None = None
    positionInitialMargin: str | None = None
    openOrderInitialMargin: str | None = None
    leverage: str | None = None
    isolated: bool | None = None
    positionSide: str | None = Field(default=None, description="BOTH, LONG or SHORT.")
    entryPrice: str | None = None
    breakEvenPrice: str | None = None
    maxQty: str | None = Field(default=None, description="Maximum quantity of base asset.")
    updateTime: int | None = None
    notionalValue: str | None = None


class CoinmAccountData(BaseModel):
    model_config = ConfigDict(extra="allow")

    assets: list[AccountAsset] | None = None
    positions: list[AccountPosition] | None = None
    canDeposit: bool | None = None
    canTrade: bool | None = None
    canWithdraw: bool | None = None
    feeTier: int | None = None
    updateTime: int | None = None


class CoinmAccountResult(ToolResult):
    data: CoinmAccountData | None = None


class AdlQuantileValues(BaseModel):
    model_config = ConfigDict(extra="allow")

    LONG: int | None = Field(default=None, description="ADL quantile for the LONG position.")
    SHORT: int | None = Field(default=None, description="ADL quantile for the SHORT position.")
    HEDGE: int | None = Field(default=None, description="Returned instead of BOTH for cross-margined positions in Hedge Mode.")
    BOTH: int | None = Field(default=None, description="ADL quantile for the One-way Mode position.")


class AdlQuantileItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    adlQuantile: AdlQuantileValues | None = Field(
        default=None, description="Quantile 0 to 4 per position side, from low to high ADL likelihood."
    )


class CoinmAdlQuantileData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[AdlQuantileItem]


class CoinmAdlQuantileResult(ToolResult):
    data: CoinmAdlQuantileData | None = None


class CoinmCommissionRateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    makerCommissionRate: str | None = None
    takerCommissionRate: str | None = None


class CoinmCommissionRateResult(ToolResult):
    data: CoinmCommissionRateData | None = None


class CoinmOpenOrderData(BaseModel):
    model_config = ConfigDict(extra="allow")

    orderId: int
    symbol: str
    avgPrice: str | None = Field(default=None, description="Average execution price.")
    clientOrderId: str | None = None
    cumBase: str | None = Field(default=None, description="Cumulative base asset amount.")
    executedQty: str | None = None
    origQty: str | None = None
    origType: str | None = None
    price: str | None = None
    reduceOnly: bool | None = None
    side: str | None = None
    positionSide: str | None = None
    status: str | None = None
    stopPrice: str | None = Field(default=None, description="Not meaningful for TRAILING_STOP_MARKET orders.")
    closePosition: bool | None = Field(default=None, description="True for a Close-All order.")
    pair: str | None = None
    time: int | None = None
    timeInForce: str | None = None
    type: str | None = None
    activatePrice: str | None = Field(default=None, description="Activation price, only returned for TRAILING_STOP_MARKET orders.")
    priceRate: str | None = Field(default=None, description="Callback rate, only returned for TRAILING_STOP_MARKET orders.")
    updateTime: int | None = None
    workingType: str | None = Field(default=None, description="Stop trigger price type.")
    priceProtect: bool | None = Field(default=None, description="Whether conditional order trigger protection is on.")
    priceMatch: str | None = Field(default=None, description="Price match mode.")
    selfTradePreventionMode: str | None = None


class CoinmOpenOrderResult(ToolResult):
    data: CoinmOpenOrderData | None = None


class CoinmOrderData(BaseModel):
    model_config = ConfigDict(extra="allow")

    orderId: int
    symbol: str
    avgPrice: str | None = Field(default=None, description="Average execution price.")
    clientOrderId: str | None = None
    cumBase: str | None = Field(default=None, description="Cumulative base asset amount.")
    executedQty: str | None = None
    origQty: str | None = None
    origType: str | None = None
    price: str | None = None
    reduceOnly: bool | None = None
    side: str | None = None
    positionSide: str | None = None
    status: str | None = None
    stopPrice: str | None = Field(default=None, description="Not meaningful for TRAILING_STOP_MARKET orders.")
    closePosition: bool | None = Field(default=None, description="True for a Close-All order.")
    pair: str | None = None
    time: int | None = None
    timeInForce: str | None = None
    type: str | None = None
    activatePrice: str | None = Field(default=None, description="Activation price, only returned for TRAILING_STOP_MARKET orders.")
    priceRate: str | None = Field(default=None, description="Callback rate, only returned for TRAILING_STOP_MARKET orders.")
    updateTime: int | None = None
    workingType: str | None = Field(default=None, description="Stop trigger price type.")
    priceProtect: bool | None = Field(default=None, description="Whether conditional order trigger protection is on.")
    priceMatch: str | None = Field(default=None, description="Price match mode.")
    selfTradePreventionMode: str | None = None


class CoinmOrderResult(ToolResult):
    data: CoinmOrderData | None = None


class CoinmPositionModeData(BaseModel):
    model_config = ConfigDict(extra="allow")

    dualSidePosition: bool | None = Field(default=None, description="True for Hedge Mode, false for One-way Mode.")


class CoinmPositionModeResult(ToolResult):
    data: CoinmPositionModeData | None = None


class AllOrdersItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    orderId: int
    symbol: str
    avgPrice: str | None = None
    clientOrderId: str | None = None
    cumBase: str | None = Field(default=None, description="Cumulative base asset amount.")
    cumQuote: str | None = Field(default=None, description="Cumulative quote asset amount.")
    executedQty: str | None = None
    origQty: str | None = None
    origType: str | None = None
    price: str | None = None
    reduceOnly: bool | None = None
    side: str | None = None
    positionSide: str | None = None
    status: str | None = None
    stopPrice: str | None = None
    closePosition: bool | None = None
    pair: str | None = None
    time: int | None = None
    timeInForce: str | None = None
    type: str | None = None
    activatePrice: str | None = Field(default=None, description="Activation price, only returned for TRAILING_STOP_MARKET orders.")
    priceRate: str | None = Field(default=None, description="Callback rate, only returned for TRAILING_STOP_MARKET orders.")
    updateTime: int | None = None
    workingType: str | None = None
    priceProtect: bool | None = None
    priceMatch: str | None = Field(default=None, description="Price match mode.")
    selfTradePreventionMode: str | None = None
    goodTillDate: int | None = Field(default=None, description="Pre-set auto cancel time for a GTD order.")


class CoinmAllOrdersListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[AllOrdersItem]


class CoinmAllOrdersListResult(ToolResult):
    data: CoinmAllOrdersListData | None = None


class BalanceItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    asset: str
    accountAlias: str | None = Field(default=None, description="Unique account code.")
    balance: str | None = None
    withdrawAvailable: str | None = Field(default=None, description="Available amount for withdrawal.")
    crossWalletBalance: str | None = None
    crossUnPnl: str | None = None
    availableBalance: str | None = None
    updateTime: int | None = None


class CoinmBalancesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[BalanceItem]


class CoinmBalancesListResult(ToolResult):
    data: CoinmBalancesListData | None = None


class ForceOrderItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    orderId: int
    symbol: str
    pair: str | None = None
    status: str | None = None
    clientOrderId: str | None = None
    price: str | None = None
    avgPrice: str | None = None
    origQty: str | None = None
    executedQty: str | None = None
    cumBase: str | None = None
    cumQuote: str | None = None
    timeInForce: str | None = None
    type: str | None = None
    reduceOnly: bool | None = None
    closePosition: bool | None = None
    side: str | None = None
    positionSide: str | None = None
    stopPrice: str | None = None
    workingType: str | None = None
    priceProtect: bool | None = None
    origType: str | None = None
    time: int | None = None
    updateTime: int | None = None
    goodTillDate: int | None = None


class CoinmForceOrdersListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[ForceOrderItem]


class CoinmForceOrdersListResult(ToolResult):
    data: CoinmForceOrdersListData | None = None


class IncomeItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str | None = None
    incomeType: str | None = None
    income: str | None = Field(default=None, description="Income amount.")
    asset: str | None = None
    info: str | None = Field(default=None, description="Extra information.")
    time: int | None = None
    tranId: str | None = Field(default=None, description="Transaction ID, unique within the same incomeType.")
    tradeId: str | None = None


class CoinmIncomeHistoryListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[IncomeItem]


class CoinmIncomeHistoryListResult(ToolResult):
    data: CoinmIncomeHistoryListData | None = None


class LeverageBracket(BaseModel):
    model_config = ConfigDict(extra="allow")

    bracket: int | None = Field(default=None, description="Bracket level.")
    initialLeverage: int | None = Field(default=None, description="Maximum leverage in this bracket.")
    qtyCap: int | None = Field(default=None, description="Upper edge of base asset quantity.")
    qtylFloor: int | None = Field(default=None, description="Lower edge of base asset quantity.")
    maintMarginRatio: float | None = None
    cum: float | None = None


class LeverageBracketItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    notionalCoef: float | None = Field(
        default=None, description="User symbol bracket multiplier, only present when the user's symbol bracket is adjusted."
    )
    brackets: list[LeverageBracket] | None = None


class CoinmLeverageBracketsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[LeverageBracketItem]


class CoinmLeverageBracketsListResult(ToolResult):
    data: CoinmLeverageBracketsListData | None = None


class OpenOrderItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    orderId: int
    symbol: str
    avgPrice: str | None = Field(default=None, description="Average execution price.")
    clientOrderId: str | None = None
    cumBase: str | None = Field(default=None, description="Cumulative base asset amount.")
    executedQty: str | None = None
    origQty: str | None = None
    origType: str | None = None
    price: str | None = None
    reduceOnly: bool | None = None
    side: str | None = None
    positionSide: str | None = None
    status: str | None = None
    stopPrice: str | None = Field(default=None, description="Not meaningful for TRAILING_STOP_MARKET orders.")
    closePosition: bool | None = Field(default=None, description="True for a Close-All order.")
    pair: str | None = None
    time: int | None = None
    timeInForce: str | None = None
    type: str | None = None
    activatePrice: str | None = Field(default=None, description="Activation price, only returned for TRAILING_STOP_MARKET orders.")
    priceRate: str | None = Field(default=None, description="Callback rate, only returned for TRAILING_STOP_MARKET orders.")
    updateTime: int | None = None
    workingType: str | None = Field(default=None, description="Stop trigger price type.")
    priceProtect: bool | None = Field(default=None, description="Whether conditional order trigger protection is on.")
    priceMatch: str | None = Field(default=None, description="Price match mode.")
    selfTradePreventionMode: str | None = None


class CoinmOpenOrdersListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[OpenOrderItem]


class CoinmOpenOrdersListResult(ToolResult):
    data: CoinmOpenOrdersListData | None = None


class AmendmentChange(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: str | None = None
    after: str | None = None


class AmendmentDetail(BaseModel):
    model_config = ConfigDict(extra="allow")

    price: AmendmentChange | None = None
    origQty: AmendmentChange | None = None
    count: int | None = None
    modifyId: int | None = Field(default=None, description="User-defined modification identifier, only returned if provided in the request.")


class AmendmentItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    orderId: int
    symbol: str
    amendmentId: int | None = Field(default=None, description="Order modification ID.")
    pair: str | None = None
    clientOrderId: str | None = None
    time: int | None = None
    amendment: AmendmentDetail | None = None


class CoinmOrderAmendmentsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[AmendmentItem]


class CoinmOrderAmendmentsListResult(ToolResult):
    data: CoinmOrderAmendmentsListData | None = None


class PositionItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    positionAmt: str | None = None
    entryPrice: str | None = None
    breakEvenPrice: str | None = None
    markPrice: str | None = None
    unRealizedProfit: str | None = None
    liquidationPrice: str | None = None
    leverage: str | None = None
    maxQty: str | None = None
    marginType: str | None = None
    isolatedMargin: str | None = None
    isAutoAddMargin: str | None = None
    positionSide: str | None = Field(default=None, description="BOTH, LONG or SHORT.")
    updateTime: int | None = None


class CoinmPositionsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[PositionItem]


class CoinmPositionsListResult(ToolResult):
    data: CoinmPositionsListData | None = None


class UserTradeItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    id: int
    orderId: int | None = None
    pair: str | None = None
    side: str | None = None
    price: str | None = None
    qty: str | None = None
    realizedPnl: str | None = None
    marginAsset: str | None = None
    baseQty: str | None = Field(default=None, description="Base asset quantity, populated for COIN-M symbols.")
    quoteQty: str | None = Field(default=None, description='Quote asset quantity, "0" for COIN-M symbols.')
    commission: str | None = Field(default=None, description="Transaction fee, in the commissionAsset.")
    commissionAsset: str | None = None
    time: int | None = None
    positionSide: str | None = None
    buyer: bool | None = Field(default=None, description="Whether the account is on the buy side of the trade.")
    maker: bool | None = Field(default=None, description="Whether the account is the maker in the trade.")


class CoinmUserTradesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[UserTradeItem]


class CoinmUserTradesListResult(ToolResult):
    data: CoinmUserTradesListData | None = None
