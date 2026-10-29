from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ._base import ToolResult


# 24hr ticker (object | array)
class Usdm24hrTickerItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    priceChange: str | None = None
    priceChangePercent: str | None = None
    weightedAvgPrice: str | None = None
    lastPrice: str | None = None
    lastQty: str | None = None
    openPrice: str | None = None
    highPrice: str | None = None
    lowPrice: str | None = None
    volume: str | None = None
    quoteVolume: str | None = None
    openTime: int | None = None
    closeTime: int | None = None
    firstId: int | None = Field(default=None, description="First trade ID in the window")
    lastId: int | None = Field(default=None, description="Last trade ID in the window")
    count: int | None = Field(default=None, description="Trade count in the window")


class Usdm24hrTickerData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = Field(
        default=None,
        description="Trade count for a single-symbol response; number of entries in items for an all-symbols response",
    )
    items: list[Usdm24hrTickerItem] | None = None
    symbol: str | None = None
    priceChange: str | None = None
    priceChangePercent: str | None = None
    weightedAvgPrice: str | None = None
    lastPrice: str | None = None
    lastQty: str | None = None
    openPrice: str | None = None
    highPrice: str | None = None
    lowPrice: str | None = None
    volume: str | None = None
    quoteVolume: str | None = None
    openTime: int | None = None
    closeTime: int | None = None
    firstId: int | None = Field(default=None, description="First trade ID in the window")
    lastId: int | None = Field(default=None, description="Last trade ID in the window")


class Usdm24hrTickerResult(ToolResult):
    data: Usdm24hrTickerData | None = None


# Asset index (object | array)
class UsdmAssetIndexItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    time: int | None = None
    index: str | None = None
    bidBuffer: str | None = None
    askBuffer: str | None = None
    bidRate: str | None = None
    askRate: str | None = None
    autoExchangeBidBuffer: str | None = None
    autoExchangeAskBuffer: str | None = None
    autoExchangeBidRate: str | None = None
    autoExchangeAskRate: str | None = None


class UsdmAssetIndexData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = None
    items: list[UsdmAssetIndexItem] | None = None
    symbol: str | None = None
    time: int | None = None
    index: str | None = None
    bidBuffer: str | None = None
    askBuffer: str | None = None
    bidRate: str | None = None
    askRate: str | None = None
    autoExchangeBidBuffer: str | None = None
    autoExchangeAskBuffer: str | None = None
    autoExchangeBidRate: str | None = None
    autoExchangeAskRate: str | None = None


class UsdmAssetIndexResult(ToolResult):
    data: UsdmAssetIndexData | None = None


# Book ticker (object | array)
class UsdmBookTickerItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    bidPrice: str | None = None
    bidQty: str | None = None
    askPrice: str | None = None
    askQty: str | None = None
    time: int | None = Field(default=None, description="Transaction time in milliseconds")
    lastUpdateId: int | None = None


class UsdmBookTickerData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = None
    items: list[UsdmBookTickerItem] | None = None
    symbol: str | None = None
    bidPrice: str | None = None
    bidQty: str | None = None
    askPrice: str | None = None
    askQty: str | None = None
    time: int | None = Field(default=None, description="Transaction time in milliseconds")
    lastUpdateId: int | None = None


class UsdmBookTickerResult(ToolResult):
    data: UsdmBookTickerData | None = None


# Composite index info (object | array)
class CompositeIndexBaseAsset(BaseModel):
    model_config = ConfigDict(extra="allow")

    baseAsset: str | None = None
    quoteAsset: str | None = None
    weightInQuantity: str | None = None
    weightInPercentage: str | None = None


class CompositeIndexInfoItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    time: int | None = Field(default=None, description="Current time in milliseconds")
    component: str | None = Field(default=None, description="Component asset")
    baseAssetList: list[CompositeIndexBaseAsset] | None = None


class UsdmCompositeIndexInfoData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = None
    items: list[CompositeIndexInfoItem] | None = None
    symbol: str | None = None
    time: int | None = Field(default=None, description="Current time in milliseconds")
    component: str | None = Field(default=None, description="Component asset")
    baseAssetList: list[CompositeIndexBaseAsset] | None = None


class UsdmCompositeIndexInfoResult(ToolResult):
    data: UsdmCompositeIndexInfoData | None = None


# Exchange info (object)
class ExchangeRateLimit(BaseModel):
    model_config = ConfigDict(extra="allow")

    interval: str | None = None
    intervalNum: int | None = None
    limit: int | None = None
    rateLimitType: str | None = None


class ExchangeAsset(BaseModel):
    model_config = ConfigDict(extra="allow")

    asset: str
    marginAvailable: bool | None = Field(
        default=None, description="Whether the asset can be used as margin in Multi-Assets mode"
    )
    autoAssetExchange: str | None = Field(
        default=None, description="Auto-exchange threshold in Multi-Assets margin mode"
    )


class ExchangeSymbol(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    pair: str | None = None
    contractType: str | None = None
    deliveryDate: int | None = None
    onboardDate: int | None = None
    status: str | None = None
    maintMarginPercent: str | None = None
    requiredMarginPercent: str | None = None
    baseAsset: str | None = None
    quoteAsset: str | None = None
    marginAsset: str | None = None
    pricePrecision: int | None = Field(
        default=None, description="Decimal places for prices; not the tick size"
    )
    quantityPrecision: int | None = Field(
        default=None, description="Decimal places for quantities; not the step size"
    )
    baseAssetPrecision: int | None = None
    quotePrecision: int | None = None
    underlyingType: str | None = None
    underlyingSubType: list[str] | None = None
    settlePlan: int | None = None
    triggerProtect: str | None = Field(
        default=None, description="Threshold for algo orders with priceProtect"
    )
    filters: list[dict[str, Any]] | None = Field(
        default=None,
        description="Symbol filters; each entry has a filterType (e.g. PRICE_FILTER, LOT_SIZE) plus filter-specific fields",
    )
    orderTypes: list[str] | None = None
    timeInForce: list[str] | None = None
    liquidationFee: str | None = Field(default=None, description="Liquidation fee rate")
    marketTakeBound: str | None = Field(
        default=None,
        description="Maximum price difference rate (from mark price) a market order can make",
    )
    maxMoveOrderLimit: int | None = None
    permissionSets: list[str] | None = None


class UsdmExchangeInfoData(BaseModel):
    model_config = ConfigDict(extra="allow")

    exchangeFilters: list[Any] | None = None
    rateLimits: list[ExchangeRateLimit] | None = None
    serverTime: int | None = Field(
        default=None, description="Server time in milliseconds; use get_usdm_server_time for the current time"
    )
    assets: list[ExchangeAsset] | None = None
    symbols: list[ExchangeSymbol] | None = None
    timezone: str | None = None
    futuresType: str | None = None


class UsdmExchangeInfoResult(ToolResult):
    data: UsdmExchangeInfoData | None = None


# Funding rate info (array root)
class FundingRateInfoItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    adjustedFundingRateCap: str | None = None
    adjustedFundingRateFloor: str | None = None
    fundingIntervalHours: int | None = None
    disclaimer: bool | None = None


class UsdmFundingRateInfoData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[FundingRateInfoItem]


class UsdmFundingRateInfoResult(ToolResult):
    data: UsdmFundingRateInfoData | None = None


# Index constituents (object)
class IndexConstituent(BaseModel):
    model_config = ConfigDict(extra="allow")

    exchange: str | None = None
    symbol: str | None = None
    price: str | None = Field(default=None, description="Constituent price; -1 for hidden TradFi perp constituents")
    weight: str | None = None


class UsdmIndexConstituentsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    time: int | None = None
    constituents: list[IndexConstituent] | None = None


class UsdmIndexConstituentsResult(ToolResult):
    data: UsdmIndexConstituentsData | None = None


# Insurance fund balance (object | array)
class InsuranceFundAsset(BaseModel):
    model_config = ConfigDict(extra="allow")

    asset: str
    marginBalance: str | None = None
    updateTime: int | None = None


class UsdmInsuranceFundItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbols: list[str] | None = None
    assets: list[InsuranceFundAsset] | None = None


class UsdmInsuranceFundBalanceData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = None
    items: list[UsdmInsuranceFundItem] | None = None
    symbols: list[str] | None = None
    assets: list[InsuranceFundAsset] | None = None


class UsdmInsuranceFundBalanceResult(ToolResult):
    data: UsdmInsuranceFundBalanceData | None = None


# Long/short ratio (array root)
class LongShortRatioItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    longShortRatio: str | None = Field(default=None, description="Long/short account number ratio of all traders")
    longAccount: str | None = Field(default=None, description="Long account number ratio of all traders")
    shortAccount: str | None = Field(default=None, description="Short account number ratio of all traders")
    timestamp: int | None = Field(default=None, description="End time of the period in milliseconds")


class UsdmLongShortRatioData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[LongShortRatioItem]


class UsdmLongShortRatioResult(ToolResult):
    data: UsdmLongShortRatioData | None = None


# Mark price (object | array)
class UsdmMarkPriceItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    markPrice: str | None = None
    indexPrice: str | None = None
    estimatedSettlePrice: str | None = Field(
        default=None, description="Estimated settle price; only useful in the last hour before settlement starts"
    )
    lastFundingRate: str | None = Field(default=None, description="Latest funding rate")
    interestRate: str | None = None
    nextFundingTime: int | None = None
    time: int | None = None


class UsdmMarkPriceData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = None
    items: list[UsdmMarkPriceItem] | None = None
    symbol: str | None = None
    markPrice: str | None = None
    indexPrice: str | None = None
    estimatedSettlePrice: str | None = Field(
        default=None, description="Estimated settle price; only useful in the last hour before settlement starts"
    )
    lastFundingRate: str | None = Field(default=None, description="Latest funding rate")
    interestRate: str | None = None
    nextFundingTime: int | None = None
    time: int | None = None


class UsdmMarkPriceResult(ToolResult):
    data: UsdmMarkPriceData | None = None


# Open interest (object)
class UsdmOpenInterestData(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    openInterest: str | None = None
    time: int | None = Field(default=None, description="Transaction time in milliseconds")


class UsdmOpenInterestResult(ToolResult):
    data: UsdmOpenInterestData | None = None


# Order book (object)
class UsdmOrderBookData(BaseModel):
    model_config = ConfigDict(extra="allow")

    lastUpdateId: int | None = None
    E: int | None = Field(default=None, description="Message output time in milliseconds")
    T: int | None = Field(default=None, description="Transaction time in milliseconds")
    bids: list[list[str]] | None = Field(default=None, description="Bid levels; each entry is [price, quantity]")
    asks: list[list[str]] | None = Field(default=None, description="Ask levels; each entry is [price, quantity]")


class UsdmOrderBookResult(ToolResult):
    data: UsdmOrderBookData | None = None


# Price ticker (object | array)
class UsdmPriceTickerItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    price: str | None = None
    time: int | None = Field(default=None, description="Transaction time in milliseconds")


class UsdmPriceTickerData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = None
    items: list[UsdmPriceTickerItem] | None = None
    symbol: str | None = None
    price: str | None = None
    time: int | None = Field(default=None, description="Transaction time in milliseconds")


class UsdmPriceTickerResult(ToolResult):
    data: UsdmPriceTickerData | None = None


# RPI order book (object)
class UsdmRpiOrderBookData(BaseModel):
    model_config = ConfigDict(extra="allow")

    lastUpdateId: int | None = None
    E: int | None = Field(default=None, description="Message output time in milliseconds")
    T: int | None = Field(default=None, description="Transaction time in milliseconds")
    bids: list[list[str]] | None = Field(default=None, description="Bid levels; each entry is [price, quantity]")
    asks: list[list[str]] | None = Field(default=None, description="Ask levels; each entry is [price, quantity]")


class UsdmRpiOrderBookResult(ToolResult):
    data: UsdmRpiOrderBookData | None = None


# Server time (object)
class UsdmServerTimeData(BaseModel):
    model_config = ConfigDict(extra="allow")

    serverTime: int


class UsdmServerTimeResult(ToolResult):
    data: UsdmServerTimeData | None = None


# Symbol ADL risk (object | array)
class UsdmSymbolAdlRiskItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    adlRisk: str | None = Field(default=None, description="ADL risk rating: high, medium or low")
    updateTime: int | None = None


class UsdmSymbolAdlRiskData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int | None = None
    items: list[UsdmSymbolAdlRiskItem] | None = None
    symbol: str | None = None
    adlRisk: str | None = Field(default=None, description="ADL risk rating: high, medium or low")
    updateTime: int | None = None


class UsdmSymbolAdlRiskResult(ToolResult):
    data: UsdmSymbolAdlRiskData | None = None


# Top trader ratios (array root)
class TopTraderAccountRatioItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    longShortRatio: str | None = Field(default=None, description="Long/short account number ratio of top traders")
    longAccount: str | None = Field(default=None, description="Long account number ratio of top traders")
    shortAccount: str | None = Field(default=None, description="Short account number ratio of top traders")
    timestamp: int | None = Field(default=None, description="End time of the period in milliseconds")


class UsdmTopTraderAccountRatioData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[TopTraderAccountRatioItem]


class UsdmTopTraderAccountRatioResult(ToolResult):
    data: UsdmTopTraderAccountRatioData | None = None


class TopTraderPositionRatioItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    longShortRatio: str | None = Field(default=None, description="Long/short position ratio of top traders")
    longAccount: str | None = Field(default=None, description="Long positions ratio of top traders")
    shortAccount: str | None = Field(default=None, description="Short positions ratio of top traders")
    timestamp: int | None = Field(default=None, description="End time of the period in milliseconds")


class UsdmTopTraderPositionRatioData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[TopTraderPositionRatioItem]


class UsdmTopTraderPositionRatioResult(ToolResult):
    data: UsdmTopTraderPositionRatioData | None = None


# Trading schedule (object)
class TradingSession(BaseModel):
    model_config = ConfigDict(extra="allow")

    startTime: int | None = None
    endTime: int | None = None
    type: str | None = Field(
        default=None,
        description="Session type: PRE_MARKET, REGULAR, AFTER_MARKET, OVERNIGHT or NO_TRADING (equity); REGULAR or NO_TRADING (other markets)",
    )


class MarketSessions(BaseModel):
    model_config = ConfigDict(extra="allow")

    sessions: list[TradingSession] | None = None


class MarketSchedules(BaseModel):
    model_config = ConfigDict(extra="allow")

    EQUITY: MarketSessions | None = Field(default=None, description="U.S. equity market")
    COMMODITY: MarketSessions | None = None
    KR_EQUITY: MarketSessions | None = Field(default=None, description="Korean equity market")
    HK_EQUITY: MarketSessions | None = Field(default=None, description="Hong Kong equity market")
    CN_EQUITY: MarketSessions | None = Field(default=None, description="China equity market")
    FX: MarketSessions | None = None


class UsdmTradingScheduleData(BaseModel):
    model_config = ConfigDict(extra="allow")

    updateTime: int | None = None
    marketSchedules: MarketSchedules | None = None


class UsdmTradingScheduleResult(ToolResult):
    data: UsdmTradingScheduleData | None = None


# Aggregate trades (array root)
class AggTradeItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    a: int = Field(description="Aggregate trade ID")
    p: str | None = Field(default=None, description="Price")
    q: str | None = Field(default=None, description="Quantity")
    nq: str | None = Field(default=None, description="Quantity excluding trades involving RPI orders")
    f: int | None = Field(default=None, description="First trade ID")
    l: int | None = Field(default=None, description="Last trade ID")
    T: int | None = Field(default=None, description="Timestamp in milliseconds")
    m: bool | None = Field(default=None, description="Whether the buyer was the maker")


class UsdmAggTradesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[AggTradeItem]


class UsdmAggTradesListResult(ToolResult):
    data: UsdmAggTradesListData | None = None


# Basis (array root)
class BasisItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    pair: str | None = None
    contractType: str | None = None
    indexPrice: str | None = None
    futuresPrice: str | None = None
    basis: str | None = None
    basisRate: str | None = None
    annualizedBasisRate: str | None = None
    timestamp: int | None = Field(default=None, description="Start time of the period in milliseconds")


class UsdmBasisListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[BasisItem]


class UsdmBasisListResult(ToolResult):
    data: UsdmBasisListData | None = None


# Klines (array of positional arrays)
class UsdmContinuousKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class UsdmContinuousKlinesListResult(ToolResult):
    data: UsdmContinuousKlinesListData | None = None


class UsdmIndexPriceKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class UsdmIndexPriceKlinesListResult(ToolResult):
    data: UsdmIndexPriceKlinesListData | None = None


class UsdmKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class UsdmKlinesListResult(ToolResult):
    data: UsdmKlinesListData | None = None


class UsdmMarkPriceKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class UsdmMarkPriceKlinesListResult(ToolResult):
    data: UsdmMarkPriceKlinesListData | None = None


class UsdmPremiumIndexKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class UsdmPremiumIndexKlinesListResult(ToolResult):
    data: UsdmPremiumIndexKlinesListData | None = None


# Delivery prices (array root)
class DeliveryPriceItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    deliveryTime: int | None = None
    deliveryPrice: float | None = None


class UsdmDeliveryPricesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[DeliveryPriceItem]


class UsdmDeliveryPricesListResult(ToolResult):
    data: UsdmDeliveryPricesListData | None = None


# Funding rate history (array root)
class FundingRateHistoryItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    fundingRate: str | None = None
    fundingTime: int | None = None
    markPrice: str | None = Field(
        default=None, description="Mark price associated with a particular funding fee charge"
    )
    rateType: str | None = Field(
        default=None,
        description="Funding rate type: Regular for the normal funding rate, Special for the additional rate generated by stock dividends",
    )


class UsdmFundingRateHistoryListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[FundingRateHistoryItem]


class UsdmFundingRateHistoryListResult(ToolResult):
    data: UsdmFundingRateHistoryListData | None = None


# Trades (array root)
class TradeItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    price: str | None = None
    qty: str | None = None
    quoteQty: str | None = None
    time: int | None = None
    isBuyerMaker: bool | None = None
    isRPITrade: bool | None = None


class UsdmHistoricalTradesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[TradeItem]


class UsdmHistoricalTradesListResult(ToolResult):
    data: UsdmHistoricalTradesListData | None = None


class UsdmRecentTradesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[TradeItem]


class UsdmRecentTradesListResult(ToolResult):
    data: UsdmRecentTradesListData | None = None


# Open interest stats (array root)
class OpenInterestStatsItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    sumOpenInterest: str | None = Field(default=None, description="Total open interest")
    sumOpenInterestValue: str | None = Field(default=None, description="Total open interest value")
    CMCCirculatingSupply: str | None = Field(default=None, description="Circulating supply provided by CMC")
    timestamp: int | None = Field(default=None, description="End time of the period in milliseconds")


class UsdmOpenInterestStatsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[OpenInterestStatsItem]


class UsdmOpenInterestStatsListResult(ToolResult):
    data: UsdmOpenInterestStatsListData | None = None


# Taker buy/sell volume (array root)
class TakerBuySellVolumeItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    buySellRatio: str | None = None
    buyVol: str | None = None
    sellVol: str | None = None
    timestamp: int | None = Field(default=None, description="Start time of the period in milliseconds")


class UsdmTakerBuySellVolumeListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[TakerBuySellVolumeItem]


class UsdmTakerBuySellVolumeListResult(ToolResult):
    data: UsdmTakerBuySellVolumeListData | None = None


# Ping
class PingUsdmData(BaseModel):
    model_config = ConfigDict(extra="allow")


class PingUsdmResult(ToolResult):
    data: PingUsdmData | None = None
