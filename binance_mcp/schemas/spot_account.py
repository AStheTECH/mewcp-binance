from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ._base import ToolResult


class CommissionRates(BaseModel):
    model_config = ConfigDict(extra="allow")

    maker: str | None = None
    taker: str | None = None
    buyer: str | None = None
    seller: str | None = None


class AccountBalance(BaseModel):
    model_config = ConfigDict(extra="allow")

    asset: str | None = None
    free: str | None = None
    locked: str | None = None


class RateLimit(BaseModel):
    model_config = ConfigDict(extra="allow")

    rateLimitType: str | None = None
    interval: str | None = None
    intervalNum: int | None = None
    limit: int | None = None
    count: int | None = None


class OrderListMember(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str | None = None
    orderId: int | None = None
    clientOrderId: str | None = None


class OrderListDetails(BaseModel):
    model_config = ConfigDict(extra="allow")

    orderListId: int
    contingencyType: str | None = None
    listStatusType: str | None = None
    listOrderStatus: str | None = None
    listClientOrderId: str | None = None
    transactionTime: int | None = None
    symbol: str | None = None
    orders: list[OrderListMember] | None = None


class OrderDetails(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    orderId: int
    orderListId: int | None = None
    clientOrderId: str | None = None
    price: str | None = None
    origQty: str | None = None
    executedQty: str | None = None
    cummulativeQuoteQty: str | None = Field(
        default=None,
        description="Cumulative quote asset quantity filled; a value below zero on some historical orders means the data is not available.",
    )
    status: str | None = None
    timeInForce: str | None = None
    type: str | None = None
    side: str | None = None
    stopPrice: str | None = None
    icebergQty: str | None = None
    time: int | None = None
    updateTime: int | None = None
    isWorking: bool | None = None
    origQuoteOrderQty: str | None = None
    workingTime: int | None = None
    selfTradePreventionMode: str | None = None
    preventedMatchId: int | None = None
    preventedQuantity: str | None = None
    strategyId: int | None = None
    strategyType: int | None = None
    trailingDelta: int | None = None
    trailingTime: int | None = None
    usedSor: bool | None = None
    workingFloor: str | None = None
    pegPriceType: str | None = None
    pegOffsetType: str | None = None
    pegOffsetValue: int | None = None
    peggedPrice: str | None = None
    expiryReason: str | None = None


class SpotAccountData(BaseModel):
    model_config = ConfigDict(extra="allow")

    makerCommission: int | None = None
    takerCommission: int | None = None
    buyerCommission: int | None = None
    sellerCommission: int | None = None
    commissionRates: CommissionRates | None = None
    canTrade: bool | None = None
    canWithdraw: bool | None = None
    canDeposit: bool | None = None
    brokered: bool | None = None
    requireSelfTradePrevention: bool | None = None
    preventSor: bool | None = None
    updateTime: int | None = None
    accountType: str | None = None
    balances: list[AccountBalance] | None = None
    permissions: list[str] | None = None
    uid: int | None = None


class SpotAccountResult(ToolResult):
    data: SpotAccountData | None = None


class CommissionDiscount(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabledForAccount: bool | None = None
    enabledForSymbol: bool | None = None
    discountAsset: str | None = None
    discount: str | None = None


class SpotCommissionRatesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    standardCommission: CommissionRates | None = None
    specialCommission: CommissionRates | None = None
    taxCommission: CommissionRates | None = None
    discount: CommissionDiscount | None = None


class SpotCommissionRatesResult(ToolResult):
    data: SpotCommissionRatesData | None = None


class SpotMyFiltersData(BaseModel):
    model_config = ConfigDict(extra="allow")

    exchangeFilters: list[dict[str, Any]] | None = None
    symbolFilters: list[dict[str, Any]] | None = None
    assetFilters: list[dict[str, Any]] | None = None
    rateLimits: list[RateLimit] | None = None


class SpotMyFiltersResult(ToolResult):
    data: SpotMyFiltersData | None = None


class SpotOrderCountUsageData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[RateLimit]


class SpotOrderCountUsageResult(ToolResult):
    data: SpotOrderCountUsageData | None = None


class SpotOrderListData(OrderListDetails):
    pass


class SpotOrderListResult(ToolResult):
    data: SpotOrderListData | None = None


class SpotOrderData(OrderDetails):
    pass


class SpotOrderResult(ToolResult):
    data: SpotOrderData | None = None


class Allocation(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    allocationId: int | None = None
    allocationType: str | None = None
    orderId: int | None = None
    orderListId: int | None = None
    price: str | None = None
    qty: str | None = None
    quoteQty: str | None = None
    commission: str | None = None
    commissionAsset: str | None = None
    time: int | None = None
    isBuyer: bool | None = None
    isMaker: bool | None = None
    isAllocator: bool | None = None


class SpotAllocationsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[Allocation]


class SpotAllocationsListResult(ToolResult):
    data: SpotAllocationsListData | None = None


class SpotAllOrderListsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[OrderListDetails]


class SpotAllOrderListsListResult(ToolResult):
    data: SpotAllOrderListsListData | None = None


class SpotAllOrdersListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[OrderDetails]


class SpotAllOrdersListResult(ToolResult):
    data: SpotAllOrdersListData | None = None


class MyTrade(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    id: int
    orderId: int | None = None
    orderListId: int | None = None
    price: str | None = None
    qty: str | None = None
    quoteQty: str | None = None
    commission: str | None = None
    commissionAsset: str | None = None
    time: int | None = None
    isBuyer: bool | None = None
    isMaker: bool | None = None
    isBestMatch: bool | None = None


class SpotMyTradesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[MyTrade]


class SpotMyTradesListResult(ToolResult):
    data: SpotMyTradesListData | None = None


class SpotOpenOrderListsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[OrderListDetails]


class SpotOpenOrderListsListResult(ToolResult):
    data: SpotOpenOrderListsListData | None = None


class SpotOpenOrdersListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[OrderDetails]


class SpotOpenOrdersListResult(ToolResult):
    data: SpotOpenOrdersListData | None = None


class OrderAmendment(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    orderId: int
    executionId: int | None = None
    origClientOrderId: str | None = None
    newClientOrderId: str | None = None
    origQty: str | None = None
    newQty: str | None = None
    time: int | None = None


class SpotOrderAmendmentsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[OrderAmendment]


class SpotOrderAmendmentsListResult(ToolResult):
    data: SpotOrderAmendmentsListData | None = None


class PreventedMatch(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    preventedMatchId: int
    takerOrderId: int | None = None
    makerSymbol: str | None = None
    makerOrderId: int | None = None
    tradeGroupId: int | None = None
    selfTradePreventionMode: str | None = None
    price: str | None = None
    makerPreventedQuantity: str | None = None
    transactTime: int | None = None


class SpotPreventedMatchesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[PreventedMatch]


class SpotPreventedMatchesListResult(ToolResult):
    data: SpotPreventedMatchesListData | None = None
