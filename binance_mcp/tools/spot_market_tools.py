"""Spot_market group: get_spot_24hr_ticker, get_spot_avg_price, get_spot_book_ticker, get_spot_order_book, get_spot_price_ticker, get_spot_reference_price, get_spot_reference_price_calculation, get_spot_rolling_window_ticker, get_spot_trading_day_ticker, list_spot_agg_trades, list_spot_historical_block_trades, list_spot_historical_trades, list_spot_klines, list_spot_recent_trades, list_spot_ui_klines"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.spot_market import (
    Spot24hrTickerData, Spot24hrTickerItem, Spot24hrTickerResult,
    SpotAggTrade, SpotAggTradesListData, SpotAggTradesListResult,
    SpotAvgPriceData, SpotAvgPriceResult,
    SpotBookTickerData, SpotBookTickerItem, SpotBookTickerResult,
    SpotHistoricalBlockTradesListData, SpotHistoricalBlockTradesListResult,
    SpotHistoricalTradesListData, SpotHistoricalTradesListResult,
    SpotKlinesListData, SpotKlinesListResult,
    SpotOrderBookData, SpotOrderBookResult,
    SpotPriceTickerData, SpotPriceTickerItem, SpotPriceTickerResult,
    SpotRecentTradesListData, SpotRecentTradesListResult,
    SpotReferencePriceCalculationData, SpotReferencePriceCalculationResult,
    SpotReferencePriceData, SpotReferencePriceResult,
    SpotRollingWindowTickerData, SpotRollingWindowTickerResult,
    SpotTradeItem,
    SpotTradingDayTickerData, SpotTradingDayTickerResult,
    SpotUiKlinesListData, SpotUiKlinesListResult,
    SpotWindowTickerItem,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("binance-mcp.tools.spot_market")

_SYMBOL_STATUSES = ("TRADING", "HALT", "BREAK", "CANCEL_ONLY")
_TICKER_TYPES = ("FULL", "MINI")
_KLINE_INTERVALS = ("1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
_WINDOW_SIZES = (
    tuple(f"{n}m" for n in range(1, 60))
    + tuple(f"{n}h" for n in range(1, 24))
    + tuple(f"{n}d" for n in range(1, 8))
)
_MAX_SYMBOLS = 100


def _bad_common(symbol, symbols, symbol_status, ticker_type):
    """Shared validation for the multi-symbol tools; returns an error message or None."""
    if symbol is not None and not symbol.strip():
        return "symbol must not be empty"
    if symbols is not None:
        if not symbols or any(not s or not s.strip() for s in symbols):
            return "symbols must be a non-empty list of non-empty strings"
        if len(symbols) > _MAX_SYMBOLS:
            return f"symbols accepts at most {_MAX_SYMBOLS} entries"
    if symbol_status is not None and symbol_status not in _SYMBOL_STATUSES:
        return f"symbol_status must be one of {', '.join(_SYMBOL_STATUSES)}"
    if ticker_type is not None and ticker_type not in _TICKER_TYPES:
        return "type must be FULL or MINI"
    return None


def _list_or_object(data, data_cls, item_cls):
    if isinstance(data, list):
        return data_cls(count=len(data), items=[item_cls(**d) for d in data])
    return data_cls(**data)


def _list_data(data, data_cls, item_factory):
    return data_cls(count=len(data), items=[item_factory(d) for d in data])


def register_spot_market_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_spot_24hr_ticker",
        description=(
            "Returns 24-hour rolling window price change statistics for one symbol, or for the symbols given in "
            "`symbols` (at most 100). With a single symbol the fields are returned directly; with `symbols` or "
            "when both are omitted they come back in `items`. Omitting both returns every symbol at request weight "
            "80, and `symbols` weighs 2 for 1-20 symbols, 40 for 21-100. `type=MINI` omits several fields."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_24hr_ticker(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BNBUSDT. Either symbol or symbols is provided; omitting both returns all symbols."),
        symbols: list[str] | None = Field(default=None, description='List of trading pair symbols, e.g. ["BTCUSDT","BNBUSDT"]. The maximum number of symbols allowed in a request is 100.'),
        type: str | None = Field(default="FULL", description="Response detail: FULL or MINI."),
        symbol_status: str | None = Field(default=None, description="Filters for symbols that have this tradingStatus: TRADING, HALT, BREAK or CANCEL_ONLY. For a single symbol, a status mismatch returns error -1220 SYMBOL_DOES_NOT_MATCH_STATUS. For multiple symbols, non-matching ones are excluded from the response."),
    ) -> Spot24hrTickerResult:
        tlog = ToolLogger(logger, "get_spot_24hr_ticker")
        msg = _bad_common(symbol, symbols, symbol_status, type)
        if msg is None and symbol is not None and symbols is not None:
            msg = "symbol and symbols cannot be used in combination"
        if msg:
            return _err(Spot24hrTickerResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/ticker/24hr", "NONE", "ticker24hr",
                                symbol=symbol, symbols=symbols, type=type, symbol_status=symbol_status)
            tlog.success()
            return Spot24hrTickerResult(success=True, statusCode=200,
                                        data=_list_or_object(data, Spot24hrTickerData, Spot24hrTickerItem))
        except Exception as exc:
            return _handle_request_exc(Spot24hrTickerResult, tlog, exc)

    @mcp.tool(
        name="get_spot_avg_price",
        description="Returns the current average price for a symbol: the average price, the interval in minutes it covers, and the last trade time.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_avg_price(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
    ) -> SpotAvgPriceResult:
        tlog = ToolLogger(logger, "get_spot_avg_price")
        if not symbol or not symbol.strip():
            return _err(SpotAvgPriceResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        try:
            data = service.call("spot", "/api/v3/avgPrice", "NONE", "avg_price", symbol=symbol)
            tlog.success()
            return SpotAvgPriceResult(success=True, statusCode=200, data=SpotAvgPriceData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotAvgPriceResult, tlog, exc)

    @mcp.tool(
        name="get_spot_book_ticker",
        description=(
            "Returns the best bid and ask price and quantity on the order book for one symbol or a list of symbols. "
            "`symbol` and `symbols` cannot be combined; with neither, every symbol is returned in `items`."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_book_ticker(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BNBUSDT. Cannot be combined with symbols; if neither is sent, book tickers for all symbols are returned."),
        symbols: list[str] | None = Field(default=None, description='List of trading pair symbols, e.g. ["BTCUSDT","BNBUSDT"]. Cannot be combined with symbol; if neither is sent, book tickers for all symbols are returned.'),
        symbol_status: str | None = Field(default=None, description="Filters for symbols that have this tradingStatus: TRADING, HALT, BREAK or CANCEL_ONLY. For a single symbol, a status mismatch returns error -1220 SYMBOL_DOES_NOT_MATCH_STATUS. For multiple or all symbols, non-matching ones are excluded from the response."),
    ) -> SpotBookTickerResult:
        tlog = ToolLogger(logger, "get_spot_book_ticker")
        msg = None
        if symbol is not None and not symbol.strip():
            msg = "symbol must not be empty"
        elif symbol is not None and symbols is not None:
            msg = "symbol and symbols cannot be used in combination"
        elif symbols is not None and (not symbols or any(not s or not s.strip() for s in symbols)):
            msg = "symbols must be a non-empty list of non-empty strings"
        elif symbol_status is not None and symbol_status not in _SYMBOL_STATUSES:
            msg = f"symbol_status must be one of {', '.join(_SYMBOL_STATUSES)}"
        if msg:
            return _err(SpotBookTickerResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/ticker/bookTicker", "NONE", "ticker_book_ticker",
                                symbol=symbol, symbols=symbols, symbol_status=symbol_status)
            tlog.success()
            return SpotBookTickerResult(success=True, statusCode=200,
                                        data=_list_or_object(data, SpotBookTickerData, SpotBookTickerItem))
        except Exception as exc:
            return _handle_request_exc(SpotBookTickerResult, tlog, exc)

    @mcp.tool(
        name="get_spot_order_book",
        description=(
            "Returns the order book depth for a symbol: lastUpdateId plus bids and asks, each entry being "
            "[price, quantity] as strings. Up to 5000 entries per side; request weight rises with "
            "limit (5 up to 100, 25 up to 500, 50 up to 1000, 250 up to 5000)."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_order_book(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        limit: int | None = Field(default=100, description="Number of entries to return. Maximum 5000."),
        symbol_status: str | None = Field(default=None, description="Filters for symbols that have this tradingStatus: TRADING, HALT, BREAK or CANCEL_ONLY. A status mismatch returns error -1220 SYMBOL_DOES_NOT_MATCH_STATUS."),
    ) -> SpotOrderBookResult:
        tlog = ToolLogger(logger, "get_spot_order_book")
        msg = None
        if not symbol or not symbol.strip():
            msg = "symbol must not be empty"
        elif limit is not None and limit > 5000:
            msg = "limit must be at most 5000"
        elif symbol_status is not None and symbol_status not in _SYMBOL_STATUSES:
            msg = f"symbol_status must be one of {', '.join(_SYMBOL_STATUSES)}"
        if msg:
            return _err(SpotOrderBookResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/depth", "NONE", "depth",
                                symbol=symbol, limit=limit, symbol_status=symbol_status)
            tlog.success()
            return SpotOrderBookResult(success=True, statusCode=200, data=SpotOrderBookData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotOrderBookResult, tlog, exc)

    @mcp.tool(
        name="get_spot_price_ticker",
        description=(
            "Returns the latest price for one symbol or a list of symbols. `symbol` and `symbols` cannot be "
            "combined; with neither, the prices of all symbols are returned in `items`."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_price_ticker(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BNBUSDT. Cannot be combined with symbols; if neither is sent, prices for all symbols are returned."),
        symbols: list[str] | None = Field(default=None, description='List of trading pair symbols, e.g. ["BTCUSDT","BNBUSDT"]. Cannot be combined with symbol; if neither is sent, prices for all symbols are returned.'),
        symbol_status: str | None = Field(default=None, description="Filters for symbols that have this tradingStatus: TRADING, HALT, BREAK or CANCEL_ONLY. For a single symbol, a status mismatch returns error -1220 SYMBOL_DOES_NOT_MATCH_STATUS. For multiple or all symbols, non-matching ones are excluded from the response."),
    ) -> SpotPriceTickerResult:
        tlog = ToolLogger(logger, "get_spot_price_ticker")
        msg = None
        if symbol is not None and not symbol.strip():
            msg = "symbol must not be empty"
        elif symbol is not None and symbols is not None:
            msg = "symbol and symbols cannot be used in combination"
        elif symbols is not None and (not symbols or any(not s or not s.strip() for s in symbols)):
            msg = "symbols must be a non-empty list of non-empty strings"
        elif symbol_status is not None and symbol_status not in _SYMBOL_STATUSES:
            msg = f"symbol_status must be one of {', '.join(_SYMBOL_STATUSES)}"
        if msg:
            return _err(SpotPriceTickerResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/ticker/price", "NONE", "ticker_price",
                                symbol=symbol, symbols=symbols, symbol_status=symbol_status)
            tlog.success()
            return SpotPriceTickerResult(success=True, statusCode=200,
                                         data=_list_or_object(data, SpotPriceTickerData, SpotPriceTickerItem))
        except Exception as exc:
            return _handle_request_exc(SpotPriceTickerResult, tlog, exc)

    @mcp.tool(
        name="get_spot_reference_price",
        description=(
            "Returns the reference price and its timestamp for a symbol. A symbol with no reference "
            "price set is rejected with code -2043."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_reference_price(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
    ) -> SpotReferencePriceResult:
        tlog = ToolLogger(logger, "get_spot_reference_price")
        if not symbol or not symbol.strip():
            return _err(SpotReferencePriceResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        try:
            data = service.call("spot", "/api/v3/referencePrice", "NONE", "reference_price", symbol=symbol)
            tlog.success()
            return SpotReferencePriceResult(success=True, statusCode=200, data=SpotReferencePriceData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotReferencePriceResult, tlog, exc)

    @mcp.tool(
        name="get_spot_reference_price_calculation",
        description=(
            "Describes how the reference price is calculated for a symbol, returning the calculation type. "
            "bucketCount and bucketWidthMs are present only for ARITHMETIC_MEAN and externalCalculationId only for EXTERNAL."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_reference_price_calculation(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        symbol_status: str | None = Field(default=None, description="Filters for symbols that have this tradingStatus: TRADING, HALT, BREAK or CANCEL_ONLY."),
    ) -> SpotReferencePriceCalculationResult:
        tlog = ToolLogger(logger, "get_spot_reference_price_calculation")
        msg = None
        if not symbol or not symbol.strip():
            msg = "symbol must not be empty"
        elif symbol_status is not None and symbol_status not in _SYMBOL_STATUSES:
            msg = f"symbol_status must be one of {', '.join(_SYMBOL_STATUSES)}"
        if msg:
            return _err(SpotReferencePriceCalculationResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/referencePrice/calculation", "NONE", "reference_price_calculation",
                                symbol=symbol, symbol_status=symbol_status)
            tlog.success()
            return SpotReferencePriceCalculationResult(success=True, statusCode=200,
                                                       data=SpotReferencePriceCalculationData(**data))
        except Exception as exc:
            return _handle_request_exc(SpotReferencePriceCalculationResult, tlog, exc)

    @mcp.tool(
        name="get_spot_rolling_window_ticker",
        description=(
            "Returns price change statistics over a rolling window (1m to 59m, 1h to 23h, 1d to 7d) for one symbol "
            "or up to 100 symbols; one of symbol or symbols is required. With `symbols` the entries come back in "
            "`items`. The actual interval can be up to 59999 ms longer than the requested window, and the weight is "
            "4 per symbol, capped at 200 above 50 symbols. This differs from the 24hr ticker."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_rolling_window_ticker(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BNBUSDT. Either symbol or symbols must be provided."),
        symbols: list[str] | None = Field(default=None, description='List of trading pair symbols, e.g. ["BTCUSDT","BNBUSDT"]. Either symbol or symbols must be provided. The maximum number of symbols allowed in a request is 100.'),
        window_size: str | None = Field(default="1d", description="Rolling window size: 1m-59m, 1h-23h or 1d-7d (e.g. 15m, 4h, 1d). Units cannot be combined (e.g. 1d2h is not allowed)."),
        type: str | None = Field(default="FULL", description="Response detail: FULL or MINI."),
        symbol_status: str | None = Field(default=None, description="Filters for symbols that have this tradingStatus: TRADING, HALT, BREAK or CANCEL_ONLY. For a single symbol, a status mismatch returns error -1220 SYMBOL_DOES_NOT_MATCH_STATUS. For multiple symbols, non-matching ones are excluded from the response."),
    ) -> SpotRollingWindowTickerResult:
        tlog = ToolLogger(logger, "get_spot_rolling_window_ticker")
        msg = _bad_common(symbol, symbols, symbol_status, type)
        if msg is None and symbol is None and symbols is None:
            msg = "Either symbol or symbols must be provided"
        elif msg is None and window_size is not None and window_size not in _WINDOW_SIZES:
            msg = "window_size must be 1m-59m, 1h-23h or 1d-7d"
        if msg:
            return _err(SpotRollingWindowTickerResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/ticker", "NONE", "ticker",
                                symbol=symbol, symbols=symbols, window_size=window_size, type=type,
                                symbol_status=symbol_status)
            tlog.success()
            return SpotRollingWindowTickerResult(
                success=True, statusCode=200,
                data=_list_or_object(data, SpotRollingWindowTickerData, SpotWindowTickerItem))
        except Exception as exc:
            return _handle_request_exc(SpotRollingWindowTickerResult, tlog, exc)

    @mcp.tool(
        name="get_spot_trading_day_ticker",
        description=(
            "Returns price change statistics for the current trading day for one symbol or up to 100 symbols; one "
            "of symbol or symbols is required. With `symbols` the entries come back in `items`. The trading day "
            "boundary follows `time_zone`, and the weight is 4 per symbol, capped at 200 above 50 symbols."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_spot_trading_day_ticker(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BNBUSDT. Either symbol or symbols must be provided."),
        symbols: list[str] | None = Field(default=None, description='List of trading pair symbols, e.g. ["BTCUSDT","BNBUSDT"]. Either symbol or symbols must be provided. The maximum number of symbols allowed in a request is 100.'),
        time_zone: str | None = Field(default="0", description="Default: 0 (UTC). Supported values: hours and minutes (e.g. -1:00, 05:45) or only hours (e.g. 0, 8, 4)."),
        type: str | None = Field(default="FULL", description="Response detail: FULL or MINI."),
        symbol_status: str | None = Field(default=None, description="Filters for symbols that have this tradingStatus: TRADING, HALT, BREAK or CANCEL_ONLY. For a single symbol, a status mismatch returns error -1220 SYMBOL_DOES_NOT_MATCH_STATUS. For multiple symbols, non-matching ones are excluded from the response."),
    ) -> SpotTradingDayTickerResult:
        tlog = ToolLogger(logger, "get_spot_trading_day_ticker")
        msg = _bad_common(symbol, symbols, symbol_status, type)
        if msg is None and symbol is None and symbols is None:
            msg = "Either symbol or symbols must be provided"
        if msg:
            return _err(SpotTradingDayTickerResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/ticker/tradingDay", "NONE", "ticker_trading_day",
                                symbol=symbol, symbols=symbols, time_zone=time_zone, type=type,
                                symbol_status=symbol_status)
            tlog.success()
            return SpotTradingDayTickerResult(
                success=True, statusCode=200,
                data=_list_or_object(data, SpotTradingDayTickerData, SpotWindowTickerItem))
        except Exception as exc:
            return _handle_request_exc(SpotTradingDayTickerResult, tlog, exc)

    @mcp.tool(
        name="list_spot_agg_trades",
        description=(
            "Lists compressed aggregate trades for a symbol, where trades that fill at the same time, from the same "
            "taker order and at the same price have their quantity aggregated. Without from_id, start_time or "
            "end_time the most recent aggregate trades are returned; at most 1000 per call."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_spot_agg_trades(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        from_id: int | None = Field(default=None, description="Aggregate trade ID to get trades from, inclusive."),
        start_time: int | None = Field(default=None, description="Timestamp in ms to get aggregate trades from, inclusive."),
        end_time: int | None = Field(default=None, description="Timestamp in ms to get aggregate trades until, inclusive."),
        limit: int | None = Field(default=500, description="Number of trades to return. Maximum 1000."),
    ) -> SpotAggTradesListResult:
        tlog = ToolLogger(logger, "list_spot_agg_trades")
        msg = None
        if not symbol or not symbol.strip():
            msg = "symbol must not be empty"
        elif limit is not None and limit > 1000:
            msg = "limit must be at most 1000"
        if msg:
            return _err(SpotAggTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/aggTrades", "NONE", "agg_trades",
                                symbol=symbol, from_id=from_id, start_time=start_time, end_time=end_time,
                                limit=limit)
            tlog.success()
            return SpotAggTradesListResult(success=True, statusCode=200,
                                           data=_list_data(data, SpotAggTradesListData, lambda d: SpotAggTrade(**d)))
        except Exception as exc:
            return _handle_request_exc(SpotAggTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_historical_block_trades",
        description=(
            "Lists block trades for a symbol starting from a given block trade ID, at most 1000 per call. "
            "Needs a Binance API key with no signature."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_spot_historical_block_trades(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        from_id: int = Field(description="Block trade ID to fetch from."),
        limit: int | None = Field(default=500, description="Number of block trades to return. Maximum 1000."),
    ) -> SpotHistoricalBlockTradesListResult:
        tlog = ToolLogger(logger, "list_spot_historical_block_trades")
        msg = None
        if not symbol or not symbol.strip():
            msg = "symbol must not be empty"
        elif limit is not None and limit > 1000:
            msg = "limit must be at most 1000"
        if msg:
            return _err(SpotHistoricalBlockTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/historicalBlockTrades", "MARKET_DATA", "historical_block_trades",
                                symbol=symbol, from_id=from_id, limit=limit)
            tlog.success()
            return SpotHistoricalBlockTradesListResult(
                success=True, statusCode=200,
                data=_list_data(data, SpotHistoricalBlockTradesListData, lambda d: SpotTradeItem(**d)))
        except Exception as exc:
            return _handle_request_exc(SpotHistoricalBlockTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_historical_trades",
        description=(
            "Lists older trades for a symbol, at most 1000 per call, starting from `from_id` or the most recent "
            "trades when it is omitted. Request weight is 25."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_spot_historical_trades(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        limit: int | None = Field(default=500, description="Number of trades to return. Maximum 1000."),
        from_id: int | None = Field(default=None, description="Trade ID to fetch from. Default gets the most recent trades."),
    ) -> SpotHistoricalTradesListResult:
        tlog = ToolLogger(logger, "list_spot_historical_trades")
        msg = None
        if not symbol or not symbol.strip():
            msg = "symbol must not be empty"
        elif limit is not None and limit > 1000:
            msg = "limit must be at most 1000"
        if msg:
            return _err(SpotHistoricalTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/historicalTrades", "NONE", "historical_trades",
                                symbol=symbol, limit=limit, from_id=from_id)
            tlog.success()
            return SpotHistoricalTradesListResult(
                success=True, statusCode=200,
                data=_list_data(data, SpotHistoricalTradesListData, lambda d: SpotTradeItem(**d)))
        except Exception as exc:
            return _handle_request_exc(SpotHistoricalTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_klines",
        description=(
            "Lists kline (candlestick) bars for a symbol and interval, at most 1000 per call, uniquely identified "
            "by open time; the most recent klines are returned when start_time and end_time are omitted. Each item "
            "is a positional array of 12 entries: [0] open time, [1] open, [2] high, [3] low, [4] close, [5] "
            "volume, [6] close time, [7] quote asset volume, [8] number of trades, [9] taker buy base asset "
            "volume, [10] taker buy quote asset volume, [11] unused."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_spot_klines(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        interval: str = Field(description="Kline interval (case-sensitive): 1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w or 1M."),
        start_time: int | None = Field(default=None, description="Start time in ms (UTC)."),
        end_time: int | None = Field(default=None, description="End time in ms (UTC)."),
        time_zone: str | None = Field(default=None, description="Default: 0 (UTC). Hours and minutes (e.g. -1:00, 05:45) or only hours (e.g. 0, 8, 4); range -12:00 to +14:00 inclusive. Intervals are interpreted in this zone while start_time and end_time stay in UTC."),
        limit: int | None = Field(default=500, description="Number of klines to return. Maximum 1000."),
    ) -> SpotKlinesListResult:
        tlog = ToolLogger(logger, "list_spot_klines")
        msg = None
        if not symbol or not symbol.strip():
            msg = "symbol must not be empty"
        elif interval not in _KLINE_INTERVALS:
            msg = f"interval must be one of {', '.join(_KLINE_INTERVALS)}"
        elif limit is not None and limit > 1000:
            msg = "limit must be at most 1000"
        if msg:
            return _err(SpotKlinesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/klines", "NONE", "klines",
                                symbol=symbol, interval=interval, start_time=start_time, end_time=end_time,
                                time_zone=time_zone, limit=limit)
            tlog.success()
            return SpotKlinesListResult(success=True, statusCode=200,
                                        data=SpotKlinesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(SpotKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_recent_trades",
        description="Lists the most recent trades for a symbol, at most 1000 per call. Returns each trade's ID, price, quantity, quote quantity, time and maker/best-match flags.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_spot_recent_trades(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        limit: int | None = Field(default=500, description="Number of trades to return. Maximum 1000."),
    ) -> SpotRecentTradesListResult:
        tlog = ToolLogger(logger, "list_spot_recent_trades")
        msg = None
        if not symbol or not symbol.strip():
            msg = "symbol must not be empty"
        elif limit is not None and limit > 1000:
            msg = "limit must be at most 1000"
        if msg:
            return _err(SpotRecentTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/trades", "NONE", "get_trades", symbol=symbol, limit=limit)
            tlog.success()
            return SpotRecentTradesListResult(
                success=True, statusCode=200,
                data=_list_data(data, SpotRecentTradesListData, lambda d: SpotTradeItem(**d)))
        except Exception as exc:
            return _handle_request_exc(SpotRecentTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_spot_ui_klines",
        description=(
            "Lists UI kline bars for a symbol and interval, at most 1000 per call: the same parameters and response "
            "shape as klines but modified data optimized for presenting candlestick charts. The most recent klines "
            "are returned when start_time and end_time are omitted. Each item is a positional array of 12 entries: "
            "[0] open time, [1] open, [2] high, [3] low, [4] close, [5] volume, [6] close time, [7] quote asset "
            "volume, [8] number of trades, [9] taker buy base asset volume, [10] taker buy quote asset volume, "
            "[11] unused."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_spot_ui_klines(
        symbol: str = Field(description="Trading pair symbol, e.g. BNBUSDT."),
        interval: str = Field(description="Kline interval (case-sensitive): 1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w or 1M."),
        start_time: int | None = Field(default=None, description="Start time in ms (UTC)."),
        end_time: int | None = Field(default=None, description="End time in ms (UTC)."),
        time_zone: str | None = Field(default="0", description="Default: 0 (UTC). Hours and minutes (e.g. -1:00, 05:45) or only hours (e.g. 0, 8, 4); range -12:00 to +14:00 inclusive. Intervals are interpreted in this zone while start_time and end_time stay in UTC."),
        limit: int | None = Field(default=500, description="Number of klines to return. Maximum 1000."),
    ) -> SpotUiKlinesListResult:
        tlog = ToolLogger(logger, "list_spot_ui_klines")
        msg = None
        if not symbol or not symbol.strip():
            msg = "symbol must not be empty"
        elif interval not in _KLINE_INTERVALS:
            msg = f"interval must be one of {', '.join(_KLINE_INTERVALS)}"
        elif limit is not None and limit > 1000:
            msg = "limit must be at most 1000"
        if msg:
            return _err(SpotUiKlinesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("spot", "/api/v3/uiKlines", "NONE", "ui_klines",
                                symbol=symbol, interval=interval, start_time=start_time, end_time=end_time,
                                time_zone=time_zone, limit=limit)
            tlog.success()
            return SpotUiKlinesListResult(success=True, statusCode=200,
                                          data=SpotUiKlinesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(SpotUiKlinesListResult, tlog, exc)
