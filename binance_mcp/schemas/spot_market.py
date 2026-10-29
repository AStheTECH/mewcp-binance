from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ._base import ToolResult


class _Model(BaseModel):
    model_config = ConfigDict(extra="allow")


# ---- 24hr ticker ----

class Spot24hrTickerItem(_Model):
    symbol: str
    priceChange: str | None = None
    priceChangePercent: str | None = None
    weightedAvgPrice: str | None = None
    prevClosePrice: str | None = None
    lastPrice: str | None = Field(default=None, description="Closing price of the interval")
    lastQty: str | None = None
    bidPrice: str | None = None
    bidQty: str | None = None
    askPrice: str | None = None
    askQty: str | None = None
    openPrice: str | None = Field(default=None, description="Opening price of the interval")
    highPrice: str | None = Field(default=None, description="Highest price in the interval")
    lowPrice: str | None = Field(default=None, description="Lowest price in the interval")
    volume: str | None = Field(default=None, description="Total trade volume in base asset")
    quoteVolume: str | None = Field(default=None, description="Total trade volume in quote asset")
    openTime: int | None = Field(default=None, description="Start of the ticker interval (ms)")
    closeTime: int | None = Field(default=None, description="End of the ticker interval (ms)")
    firstId: int | None = Field(default=None, description="First trade ID")
    lastId: int | None = Field(default=None, description="Last trade ID")
    count: int | None = Field(default=None, description="Trade count")


class Spot24hrTickerData(Spot24hrTickerItem):
    symbol: str | None = None
    items: list[Spot24hrTickerItem] | None = Field(
        default=None, description="Present when the response is a list (symbols sent or both omitted)"
    )
    count: int | None = Field(
        default=None, description="Trade count for a single symbol, or the number of items for a list response"
    )


class Spot24hrTickerResult(ToolResult):
    data: Spot24hrTickerData | None = None


# ---- avg price ----

class SpotAvgPriceData(_Model):
    mins: int | None = Field(default=None, description="Average price interval in minutes")
    price: str | None = Field(default=None, description="Average price")
    closeTime: int | None = Field(default=None, description="Last trade time (ms)")


class SpotAvgPriceResult(ToolResult):
    data: SpotAvgPriceData | None = None


# ---- book ticker ----

class SpotBookTickerItem(_Model):
    symbol: str
    bidPrice: str | None = Field(default=None, description="Best bid price")
    bidQty: str | None = Field(default=None, description="Quantity at the best bid")
    askPrice: str | None = Field(default=None, description="Best ask price")
    askQty: str | None = Field(default=None, description="Quantity at the best ask")


class SpotBookTickerData(SpotBookTickerItem):
    symbol: str | None = None
    items: list[SpotBookTickerItem] | None = None
    count: int | None = Field(default=None, description="Number of items for a list response")


class SpotBookTickerResult(ToolResult):
    data: SpotBookTickerData | None = None


# ---- order book ----

class SpotOrderBookData(_Model):
    lastUpdateId: int | None = None
    bids: list[list[str]] | None = Field(default=None, description="Each entry is [price, quantity]")
    asks: list[list[str]] | None = Field(default=None, description="Each entry is [price, quantity]")


class SpotOrderBookResult(ToolResult):
    data: SpotOrderBookData | None = None


# ---- price ticker ----

class SpotPriceTickerItem(_Model):
    symbol: str
    price: str | None = None


class SpotPriceTickerData(SpotPriceTickerItem):
    symbol: str | None = None
    items: list[SpotPriceTickerItem] | None = None
    count: int | None = Field(default=None, description="Number of items for a list response")


class SpotPriceTickerResult(ToolResult):
    data: SpotPriceTickerData | None = None


# ---- reference price ----

class SpotReferencePriceData(_Model):
    symbol: str | None = None
    referencePrice: str | None = None
    timestamp: int | None = None


class SpotReferencePriceResult(ToolResult):
    data: SpotReferencePriceData | None = None


class SpotReferencePriceCalculationData(_Model):
    symbol: str | None = None
    calculationType: str | None = Field(
        default=None, description="How the reference price is calculated, e.g. ARITHMETIC_MEAN or EXTERNAL"
    )
    bucketCount: int | None = Field(default=None, description="Only returned for ARITHMETIC_MEAN")
    bucketWidthMs: int | None = Field(default=None, description="Only returned for ARITHMETIC_MEAN")
    externalCalculationId: int | None = Field(default=None, description="Only returned for EXTERNAL")


class SpotReferencePriceCalculationResult(ToolResult):
    data: SpotReferencePriceCalculationData | None = None


# ---- rolling window / trading day tickers ----

class SpotWindowTickerItem(_Model):
    symbol: str
    priceChange: str | None = None
    priceChangePercent: str | None = None
    weightedAvgPrice: str | None = None
    openPrice: str | None = Field(default=None, description="Opening price of the interval")
    highPrice: str | None = Field(default=None, description="Highest price in the interval")
    lowPrice: str | None = Field(default=None, description="Lowest price in the interval")
    lastPrice: str | None = Field(default=None, description="Closing price of the interval")
    volume: str | None = Field(default=None, description="Total trade volume in base asset")
    quoteVolume: str | None = Field(default=None, description="Total trade volume in quote asset")
    openTime: int | None = Field(default=None, description="Start of the ticker interval (ms)")
    closeTime: int | None = Field(default=None, description="End of the ticker interval (ms)")
    firstId: int | None = Field(default=None, description="First trade ID")
    lastId: int | None = Field(default=None, description="Last trade ID")
    count: int | None = Field(default=None, description="Trade count")


class _WindowTickerData(SpotWindowTickerItem):
    symbol: str | None = None
    items: list[SpotWindowTickerItem] | None = Field(
        default=None, description="Present when the response is a list (symbols sent)"
    )
    count: int | None = Field(
        default=None, description="Trade count for a single symbol, or the number of items for a list response"
    )


class SpotRollingWindowTickerData(_WindowTickerData):
    pass


class SpotRollingWindowTickerResult(ToolResult):
    data: SpotRollingWindowTickerData | None = None


class SpotTradingDayTickerData(_WindowTickerData):
    pass


class SpotTradingDayTickerResult(ToolResult):
    data: SpotTradingDayTickerData | None = None


# ---- aggregate trades ----

class SpotAggTrade(_Model):
    a: int | None = Field(default=None, description="Aggregate trade ID")
    p: str | None = Field(default=None, description="Price")
    q: str | None = Field(default=None, description="Quantity")
    f: int | None = Field(default=None, description="First trade ID")
    l: int | None = Field(default=None, description="Last trade ID")
    T: int | None = Field(default=None, description="Trade time (ms)")
    m: bool | None = Field(default=None, description="Whether the buyer was the maker")
    M: bool | None = Field(default=None, description="Whether the trade was the best price match")


class SpotAggTradesListData(_Model):
    count: int
    items: list[SpotAggTrade]


class SpotAggTradesListResult(ToolResult):
    data: SpotAggTradesListData | None = None


# ---- trades ----

class SpotTradeItem(_Model):
    id: int
    price: str | None = None
    qty: str | None = None
    quoteQty: str | None = None
    time: int | None = Field(default=None, description="Trade time (ms)")
    isBuyerMaker: bool | None = None
    isBestMatch: bool | None = None


class SpotHistoricalBlockTradesListData(_Model):
    count: int
    items: list[SpotTradeItem]


class SpotHistoricalBlockTradesListResult(ToolResult):
    data: SpotHistoricalBlockTradesListData | None = None


class SpotHistoricalTradesListData(_Model):
    count: int
    items: list[SpotTradeItem]


class SpotHistoricalTradesListResult(ToolResult):
    data: SpotHistoricalTradesListData | None = None


class SpotRecentTradesListData(_Model):
    count: int
    items: list[SpotTradeItem]


class SpotRecentTradesListResult(ToolResult):
    data: SpotRecentTradesListData | None = None


# ---- klines ----

class SpotKlinesListData(_Model):
    count: int
    items: list[list[Any]]


class SpotKlinesListResult(ToolResult):
    data: SpotKlinesListData | None = None


class SpotUiKlinesListData(_Model):
    count: int
    items: list[list[Any]]


class SpotUiKlinesListResult(ToolResult):
    data: SpotUiKlinesListData | None = None
