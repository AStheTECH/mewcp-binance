from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ._base import ToolResult


# ---- get_coinm_24hr_ticker ----

class Coinm24hrTickerItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    pair: str | None = None
    priceChange: str | None = None
    priceChangePercent: str | None = None
    weightedAvgPrice: str | None = None
    lastPrice: str | None = None
    lastQty: str | None = None
    openPrice: str | None = None
    highPrice: str | None = None
    lowPrice: str | None = None
    volume: str | None = None
    baseVolume: str | None = None
    openTime: int | None = Field(default=None, description="Start time of the 24h window (milliseconds).")
    closeTime: int | None = Field(default=None, description="End time of the 24h window (milliseconds).")
    firstId: int | None = None
    lastId: int | None = None
    count: int | None = Field(default=None, description="Total number of trades in the 24h window.")


class Coinm24hrTickerData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[Coinm24hrTickerItem]


class Coinm24hrTickerResult(ToolResult):
    data: Coinm24hrTickerData | None = None


# ---- get_coinm_book_ticker ----

class CoinmBookTickerItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    pair: str | None = None
    lastUpdateId: int | None = None
    bidPrice: str | None = None
    bidQty: str | None = None
    askPrice: str | None = None
    askQty: str | None = None
    time: int | None = None


class CoinmBookTickerData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmBookTickerItem]


class CoinmBookTickerResult(ToolResult):
    data: CoinmBookTickerData | None = None


# ---- get_coinm_exchange_info ----

class CoinmRateLimit(BaseModel):
    model_config = ConfigDict(extra="allow")

    interval: str | None = None
    intervalNum: int | None = None
    limit: int | None = None
    rateLimitType: str | None = None


class CoinmSymbolFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    filterType: str | None = Field(default=None, description="Filter type; determines which of the other fields are present.")
    maxPrice: str | None = None
    minPrice: str | None = None
    tickSize: str | None = None
    maxQty: str | None = Field(default=None, description="Maximum quantity of base asset.")
    minQty: str | None = None
    stepSize: str | None = None
    limit: int | None = None
    multiplierUp: str | None = None
    multiplierDown: str | None = None
    multiplierDecimal: str | None = None


class CoinmSymbolInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    pair: str | None = None
    contractType: str | None = None
    deliveryDate: int | None = None
    onboardDate: int | None = None
    contractStatus: str | None = None
    contractSize: int | None = None
    quoteAsset: str | None = None
    baseAsset: str | None = None
    marginAsset: str | None = None
    pricePrecision: int | None = Field(default=None, description="Not a tick size; use the PRICE_FILTER tickSize instead.")
    quantityPrecision: int | None = Field(default=None, description="Not a step size; use the LOT_SIZE stepSize instead.")
    baseAssetPrecision: int | None = None
    quotePrecision: int | None = None
    equalQtyPrecision: int | None = None
    triggerProtect: str | None = Field(default=None, description="Threshold for algo orders with priceProtect.")
    maintMarginPercent: str | None = None
    requiredMarginPercent: str | None = None
    underlyingType: str | None = None
    underlyingSubType: list[str] | None = None
    liquidationFee: str | None = Field(default=None, description="Liquidation fee rate.")
    marketTakeBound: str | None = Field(default=None, description="Maximum price difference rate from the mark price that a market order can make.")
    filters: list[CoinmSymbolFilter] | None = None
    orderTypes: list[str] | None = None
    timeInForce: list[str] | None = None


class CoinmExchangeInfoData(BaseModel):
    model_config = ConfigDict(extra="allow")

    timezone: str | None = None
    serverTime: int | None = Field(default=None, description="Not intended for use; call get_coinm_server_time for the current server time.")
    exchangeFilters: list[Any] | None = None
    rateLimits: list[CoinmRateLimit] | None = None
    symbols: list[CoinmSymbolInfo] | None = None


class CoinmExchangeInfoResult(ToolResult):
    data: CoinmExchangeInfoData | None = None


# ---- get_coinm_funding_rate_info ----

class CoinmFundingRateInfoItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    adjustedFundingRateCap: str | None = None
    adjustedFundingRateFloor: str | None = None
    fundingIntervalHours: int | None = None
    disclaimer: bool | None = None


class CoinmFundingRateInfoData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmFundingRateInfoItem]


class CoinmFundingRateInfoResult(ToolResult):
    data: CoinmFundingRateInfoData | None = None


# ---- get_coinm_index_constituents ----

class CoinmIndexConstituent(BaseModel):
    model_config = ConfigDict(extra="allow")

    exchange: str | None = None
    symbol: str | None = None
    price: str | None = None
    weight: str | None = None


class CoinmIndexConstituentsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    time: int | None = None
    constituents: list[CoinmIndexConstituent] | None = None


class CoinmIndexConstituentsResult(ToolResult):
    data: CoinmIndexConstituentsData | None = None


# ---- get_coinm_long_short_ratio ----

class CoinmLongShortRatioItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    pair: str | None = None
    longShortRatio: str | None = None
    longAccount: str | None = Field(default=None, description="Share of accounts net long, as a decimal fraction (0.6442 = 64.42%).")
    shortAccount: str | None = Field(default=None, description="Share of accounts net short, as a decimal fraction (0.3558 = 35.58%).")
    timestamp: int | None = Field(default=None, description="End time of the period, in milliseconds.")


class CoinmLongShortRatioData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmLongShortRatioItem]


class CoinmLongShortRatioResult(ToolResult):
    data: CoinmLongShortRatioData | None = None


# ---- get_coinm_mark_price ----

class CoinmMarkPriceItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    pair: str | None = None
    markPrice: str | None = None
    indexPrice: str | None = None
    estimatedSettlePrice: str | None = Field(default=None, description="Estimated settle price, only useful in the last hour before settlement starts.")
    lastFundingRate: str | None = Field(default=None, description="Latest funding rate; perpetual symbols only, empty string for delivery symbols.")
    interestRate: str | None = Field(default=None, description="Base asset interest rate; perpetual symbols only, empty string for delivery symbols.")
    nextFundingTime: int | None = Field(default=None, description="Perpetual symbols only; 0 for delivery symbols.")
    time: int | None = None


class CoinmMarkPriceData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmMarkPriceItem]


class CoinmMarkPriceResult(ToolResult):
    data: CoinmMarkPriceData | None = None


# ---- get_coinm_open_interest ----

class CoinmOpenInterestData(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    pair: str | None = None
    openInterest: str | None = None
    contractType: str | None = None
    time: int | None = None


class CoinmOpenInterestResult(ToolResult):
    data: CoinmOpenInterestData | None = None


# ---- get_coinm_order_book ----

class CoinmOrderBookData(BaseModel):
    model_config = ConfigDict(extra="allow")

    lastUpdateId: int | None = None
    symbol: str | None = None
    pair: str | None = None
    E: int | None = Field(default=None, description="Message output time.")
    T: int | None = Field(default=None, description="Transaction time.")
    bids: list[list[str]] | None = Field(default=None, description="Bid orders; each entry is [price, quantity].")
    asks: list[list[str]] | None = Field(default=None, description="Ask orders; each entry is [price, quantity].")


class CoinmOrderBookResult(ToolResult):
    data: CoinmOrderBookData | None = None


# ---- get_coinm_price_ticker ----

class CoinmPriceTickerItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    ps: str | None = Field(default=None, description="Pair.")
    price: str | None = None
    time: int | None = None


class CoinmPriceTickerData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmPriceTickerItem]


class CoinmPriceTickerResult(ToolResult):
    data: CoinmPriceTickerData | None = None


# ---- get_coinm_server_time ----

class CoinmServerTimeData(BaseModel):
    model_config = ConfigDict(extra="allow")

    serverTime: int | None = Field(default=None, description="Current server time in milliseconds.")


class CoinmServerTimeResult(ToolResult):
    data: CoinmServerTimeData | None = None


# ---- get_coinm_top_trader_account_ratio ----

class CoinmTopTraderAccountRatioItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    pair: str | None = None
    longShortRatio: str | None = None
    longAccount: str | None = Field(default=None, description="Share of top-trader accounts net long, as a decimal fraction (0.6442 = 64.42%).")
    shortAccount: str | None = Field(default=None, description="Share of top-trader accounts net short, as a decimal fraction (0.3558 = 35.58%).")
    timestamp: int | None = Field(default=None, description="End time of the period, in milliseconds.")


class CoinmTopTraderAccountRatioData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmTopTraderAccountRatioItem]


class CoinmTopTraderAccountRatioResult(ToolResult):
    data: CoinmTopTraderAccountRatioData | None = None


# ---- get_coinm_top_trader_position_ratio ----

class CoinmTopTraderPositionRatioItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    pair: str | None = None
    longShortRatio: str | None = None
    longPosition: str | None = Field(default=None, description="Share of top-trader open positions that are long, as a decimal fraction.")
    shortPosition: str | None = Field(default=None, description="Share of top-trader open positions that are short, as a decimal fraction.")
    timestamp: int | None = Field(default=None, description="End time of the period, in milliseconds.")


class CoinmTopTraderPositionRatioData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmTopTraderPositionRatioItem]


class CoinmTopTraderPositionRatioResult(ToolResult):
    data: CoinmTopTraderPositionRatioData | None = None


# ---- list_coinm_agg_trades ----

class CoinmAggTradeItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    a: int = Field(description="Aggregate trade ID.")
    p: str | None = Field(default=None, description="Price.")
    q: str | None = Field(default=None, description="Quantity.")
    f: int | None = Field(default=None, description="First trade ID.")
    l: int | None = Field(default=None, description="Last trade ID.")
    T: int | None = Field(default=None, description="Timestamp in milliseconds.")
    m: bool | None = Field(default=None, description="Whether the buyer was the maker.")


class CoinmAggTradesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmAggTradeItem]


class CoinmAggTradesListResult(ToolResult):
    data: CoinmAggTradesListData | None = None


# ---- list_coinm_basis ----

class CoinmBasisItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    pair: str | None = None
    contractType: str | None = None
    indexPrice: str | None = None
    futuresPrice: str | None = None
    basis: str | None = None
    basisRate: str | None = None
    annualizedBasisRate: str | None = None
    timestamp: int | None = Field(default=None, description="Start time of the period, in milliseconds.")


class CoinmBasisListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmBasisItem]


class CoinmBasisListResult(ToolResult):
    data: CoinmBasisListData | None = None


# ---- kline tools ----

class CoinmContinuousKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class CoinmContinuousKlinesListResult(ToolResult):
    data: CoinmContinuousKlinesListData | None = None


class CoinmIndexPriceKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class CoinmIndexPriceKlinesListResult(ToolResult):
    data: CoinmIndexPriceKlinesListData | None = None


class CoinmKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class CoinmKlinesListResult(ToolResult):
    data: CoinmKlinesListData | None = None


class CoinmMarkPriceKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class CoinmMarkPriceKlinesListResult(ToolResult):
    data: CoinmMarkPriceKlinesListData | None = None


class CoinmPremiumIndexKlinesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[list[Any]]


class CoinmPremiumIndexKlinesListResult(ToolResult):
    data: CoinmPremiumIndexKlinesListData | None = None


# ---- list_coinm_funding_rate_history ----

class CoinmFundingRateHistoryItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str | None = None
    fundingTime: int | None = None
    fundingRate: str | None = None


class CoinmFundingRateHistoryListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmFundingRateHistoryItem]


class CoinmFundingRateHistoryListResult(ToolResult):
    data: CoinmFundingRateHistoryListData | None = None


# ---- trades (historical / recent) ----

class CoinmTradeItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    price: str | None = None
    qty: str | None = Field(default=None, description="Quantity in contracts.")
    baseQty: str | None = Field(default=None, description="Quantity in base asset.")
    time: int | None = None
    isBuyerMaker: bool | None = None


class CoinmHistoricalTradesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmTradeItem]


class CoinmHistoricalTradesListResult(ToolResult):
    data: CoinmHistoricalTradesListData | None = None


class CoinmRecentTradesListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmTradeItem]


class CoinmRecentTradesListResult(ToolResult):
    data: CoinmRecentTradesListData | None = None


# ---- list_coinm_open_interest_stats ----

class CoinmOpenInterestStatsItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    pair: str | None = None
    contractType: str | None = None
    sumOpenInterest: str | None = Field(default=None, description="Open interest in contracts.")
    sumOpenInterestValue: str | None = Field(default=None, description="Open interest value in base asset.")
    timestamp: int | None = Field(default=None, description="End time of the period, in milliseconds.")


class CoinmOpenInterestStatsListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmOpenInterestStatsItem]


class CoinmOpenInterestStatsListResult(ToolResult):
    data: CoinmOpenInterestStatsListData | None = None


# ---- list_coinm_taker_buy_sell_volume ----

class CoinmTakerBuySellVolumeItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    pair: str | None = None
    contractType: str | None = None
    takerBuyVol: str | None = Field(default=None, description="Taker buy volume in contracts.")
    takerSellVol: str | None = Field(default=None, description="Taker sell volume in contracts.")
    takerBuyVolValue: str | None = Field(default=None, description="Taker buy volume in base asset.")
    takerSellVolValue: str | None = Field(default=None, description="Taker sell volume in base asset.")
    timestamp: int | None = Field(default=None, description="Start time of the period, in milliseconds.")


class CoinmTakerBuySellVolumeListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    items: list[CoinmTakerBuySellVolumeItem]


class CoinmTakerBuySellVolumeListResult(ToolResult):
    data: CoinmTakerBuySellVolumeListData | None = None


# ---- ping_coinm ----

class PingCoinmData(BaseModel):
    model_config = ConfigDict(extra="allow")


class PingCoinmResult(ToolResult):
    data: PingCoinmData | None = None
