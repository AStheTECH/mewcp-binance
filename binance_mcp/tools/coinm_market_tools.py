"""coinm_market group: get_coinm_24hr_ticker, get_coinm_book_ticker, get_coinm_exchange_info, get_coinm_funding_rate_info, get_coinm_index_constituents, get_coinm_long_short_ratio, get_coinm_mark_price, get_coinm_open_interest, get_coinm_order_book, get_coinm_price_ticker, get_coinm_server_time, get_coinm_top_trader_account_ratio, get_coinm_top_trader_position_ratio, list_coinm_agg_trades, list_coinm_basis, list_coinm_continuous_klines, list_coinm_funding_rate_history, list_coinm_historical_trades, list_coinm_index_price_klines, list_coinm_klines, list_coinm_mark_price_klines, list_coinm_open_interest_stats, list_coinm_premium_index_klines, list_coinm_recent_trades, list_coinm_taker_buy_sell_volume, ping_coinm"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.coinm_market import (
    Coinm24hrTickerData,
    Coinm24hrTickerResult,
    CoinmAggTradesListData,
    CoinmAggTradesListResult,
    CoinmBasisListData,
    CoinmBasisListResult,
    CoinmBookTickerData,
    CoinmBookTickerResult,
    CoinmContinuousKlinesListData,
    CoinmContinuousKlinesListResult,
    CoinmExchangeInfoData,
    CoinmExchangeInfoResult,
    CoinmFundingRateHistoryListData,
    CoinmFundingRateHistoryListResult,
    CoinmFundingRateInfoData,
    CoinmFundingRateInfoResult,
    CoinmHistoricalTradesListData,
    CoinmHistoricalTradesListResult,
    CoinmIndexConstituentsData,
    CoinmIndexConstituentsResult,
    CoinmIndexPriceKlinesListData,
    CoinmIndexPriceKlinesListResult,
    CoinmKlinesListData,
    CoinmKlinesListResult,
    CoinmLongShortRatioData,
    CoinmLongShortRatioResult,
    CoinmMarkPriceData,
    CoinmMarkPriceKlinesListData,
    CoinmMarkPriceKlinesListResult,
    CoinmMarkPriceResult,
    CoinmOpenInterestData,
    CoinmOpenInterestResult,
    CoinmOpenInterestStatsListData,
    CoinmOpenInterestStatsListResult,
    CoinmOrderBookData,
    CoinmOrderBookResult,
    CoinmPremiumIndexKlinesListData,
    CoinmPremiumIndexKlinesListResult,
    CoinmPriceTickerData,
    CoinmPriceTickerResult,
    CoinmRecentTradesListData,
    CoinmRecentTradesListResult,
    CoinmServerTimeData,
    CoinmServerTimeResult,
    CoinmTakerBuySellVolumeListData,
    CoinmTakerBuySellVolumeListResult,
    CoinmTopTraderAccountRatioData,
    CoinmTopTraderAccountRatioResult,
    CoinmTopTraderPositionRatioData,
    CoinmTopTraderPositionRatioResult,
    PingCoinmData,
    PingCoinmResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("binance-mcp.tools.coinm_market")

_PERIODS = ["5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"]
_INTERVALS = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
_CONTRACT_TYPES = ["PERPETUAL", "CURRENT_QUARTER", "NEXT_QUARTER"]
_CONTRACT_TYPES_ALL = ["ALL", *_CONTRACT_TYPES]
_BOOK_LIMITS = [5, 10, 20, 50, 100, 500, 1000]


def _in(name: str, value: Any, allowed: list) -> str | None:
    if value is not None and value not in allowed:
        return f"{name} must be one of: {', '.join(str(a) for a in allowed)}"
    return None


def _max(name: str, value: int | None, maximum: int) -> str | None:
    if value is not None and not 1 <= value <= maximum:
        return f"{name} must be between 1 and {maximum}"
    return None


def _blank(name: str, value: str | None) -> str | None:
    if value is None or not value.strip():
        return f"{name} must not be empty"
    return None


def register_coinm_market_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_coinm_24hr_ticker",
        description=(
            "Returns 24-hour rolling price change statistics for one COIN-M futures symbol, all symbols of a "
            "pair, or all symbols when both are omitted. Symbol and pair cannot be sent together; request "
            "weight is 1 for a single symbol and 40 when symbol is omitted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_24hr_ticker(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSD_PERP. Cannot be combined with pair. Omit both to return all symbols."),
        pair: str | None = Field(default=None, description="Pair, e.g. BTCUSD. Cannot be combined with symbol. Omit both to return all symbols."),
    ) -> Coinm24hrTickerResult:
        tlog = ToolLogger(logger, "get_coinm_24hr_ticker")
        if symbol and pair:
            return _err(Coinm24hrTickerResult, tlog, "VALIDATION_ERROR", "symbol and pair cannot be sent together", 400)
        try:
            data = service.call("coinm", "/dapi/v1/ticker/24hr", "NONE", "ticker24hr_price_change_statistics", symbol=symbol, pair=pair)
            tlog.success()
            return Coinm24hrTickerResult(success=True, statusCode=200, data=Coinm24hrTickerData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(Coinm24hrTickerResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_book_ticker",
        description=(
            "Returns the best bid and ask price and quantity on the order book for one COIN-M futures symbol, "
            "all symbols of a pair, or all symbols when both are omitted. Symbol and pair cannot be sent "
            "together; request weight is 2 for a single symbol and 5 when symbol is omitted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_book_ticker(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSD_PERP. Cannot be combined with pair. Omit both to return all symbols."),
        pair: str | None = Field(default=None, description="Pair, e.g. BTCUSD. Cannot be combined with symbol. Omit both to return all symbols."),
    ) -> CoinmBookTickerResult:
        tlog = ToolLogger(logger, "get_coinm_book_ticker")
        if symbol and pair:
            return _err(CoinmBookTickerResult, tlog, "VALIDATION_ERROR", "symbol and pair cannot be sent together", 400)
        try:
            data = service.call("coinm", "/dapi/v1/ticker/bookTicker", "NONE", "symbol_order_book_ticker", symbol=symbol, pair=pair)
            tlog.success()
            return CoinmBookTickerResult(success=True, statusCode=200, data=CoinmBookTickerData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmBookTickerResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_exchange_info",
        description=(
            "Returns COIN-M futures exchange trading rules, rate limits and symbol information including "
            "filters, contract types and precisions."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_exchange_info(
    ) -> CoinmExchangeInfoResult:
        tlog = ToolLogger(logger, "get_coinm_exchange_info")
        try:
            data = service.call("coinm", "/dapi/v1/exchangeInfo", "NONE", "exchange_information")
            tlog.success()
            return CoinmExchangeInfoResult(success=True, statusCode=200, data=CoinmExchangeInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(CoinmExchangeInfoResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_funding_rate_info",
        description=(
            "Returns funding rate cap, floor and interval hours for COIN-M symbols whose funding parameters "
            "were adjusted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_funding_rate_info(
    ) -> CoinmFundingRateInfoResult:
        tlog = ToolLogger(logger, "get_coinm_funding_rate_info")
        try:
            data = service.call("coinm", "/dapi/v1/fundingInfo", "NONE", "get_funding_rate_info")
            tlog.success()
            return CoinmFundingRateInfoResult(success=True, statusCode=200, data=CoinmFundingRateInfoData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmFundingRateInfoResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_index_constituents",
        description=(
            "Returns the exchanges, prices and weights that make up the index price of a COIN-M futures "
            "symbol."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_index_constituents(
        symbol: str = Field(description="Index symbol, e.g. BTCUSD."),
    ) -> CoinmIndexConstituentsResult:
        tlog = ToolLogger(logger, "get_coinm_index_constituents")
        msg = _blank("symbol", symbol)
        if msg:
            return _err(CoinmIndexConstituentsResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/constituents", "NONE", "query_index_price_constituents", symbol=symbol)
            tlog.success()
            return CoinmIndexConstituentsResult(success=True, statusCode=200, data=CoinmIndexConstituentsData(**data))
        except Exception as exc:
            return _handle_request_exc(CoinmIndexConstituentsResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_long_short_ratio",
        description=(
            "Returns the global long/short account ratio history for a COIN-M pair at the chosen period. Only "
            "the latest 30 days are available; without startTime and endTime the most recent data is "
            "returned."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_long_short_ratio(
        pair: str = Field(description="COIN-M pair, e.g. BTCUSD."),
        period: str = Field(description="Period of each data point: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h or 1d."),
        contract_type: str | None = Field(default=None, description="Contract type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER. Omit to aggregate across all contract types."),
        limit: int = Field(default=30, description="Maximum number of records to return, up to 500. Defaults to 30."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
    ) -> CoinmLongShortRatioResult:
        tlog = ToolLogger(logger, "get_coinm_long_short_ratio")
        msg = (_blank("pair", pair)
            or _in("period", period, _PERIODS)
            or _in("contract_type", contract_type, _CONTRACT_TYPES)
            or _max("limit", limit, 500))
        if msg:
            return _err(CoinmLongShortRatioResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/futures/data/globalLongShortAccountRatio", "NONE", "long_short_ratio", pair=pair, period=period, contract_type=contract_type, limit=limit, start_time=start_time, end_time=end_time)
            tlog.success()
            return CoinmLongShortRatioResult(success=True, statusCode=200, data=CoinmLongShortRatioData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmLongShortRatioResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_mark_price",
        description=(
            "Returns mark price, index price, estimated settle price and funding data for one COIN-M futures "
            "symbol, all symbols of a pair, or all symbols when both are omitted. Funding fields apply to "
            "perpetual symbols only."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_mark_price(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSD_PERP. Omit to return all symbols."),
        pair: str | None = Field(default=None, description="Pair, e.g. BTCUSD. Returns all symbols of the pair."),
    ) -> CoinmMarkPriceResult:
        tlog = ToolLogger(logger, "get_coinm_mark_price")
        try:
            data = service.call("coinm", "/dapi/v1/premiumIndex", "NONE", "index_price_and_mark_price", symbol=symbol, pair=pair)
            tlog.success()
            return CoinmMarkPriceResult(success=True, statusCode=200, data=CoinmMarkPriceData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmMarkPriceResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_open_interest",
        description=(
            "Returns the present open interest of a COIN-M futures symbol."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_open_interest(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP."),
    ) -> CoinmOpenInterestResult:
        tlog = ToolLogger(logger, "get_coinm_open_interest")
        msg = _blank("symbol", symbol)
        if msg:
            return _err(CoinmOpenInterestResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/openInterest", "NONE", "open_interest", symbol=symbol)
            tlog.success()
            return CoinmOpenInterestResult(success=True, statusCode=200, data=CoinmOpenInterestData(**data))
        except Exception as exc:
            return _handle_request_exc(CoinmOpenInterestResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_order_book",
        description=(
            "Returns the order book bids and asks for a COIN-M futures symbol; each entry is [price, "
            "quantity]. Request weight depends on limit: 2 for 5-50, 5 for 100, 10 for 500, 20 for 1000."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_order_book(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP."),
        limit: int = Field(default=500, description="Number of price levels per side: 5, 10, 20, 50, 100, 500 or 1000. Defaults to 500."),
    ) -> CoinmOrderBookResult:
        tlog = ToolLogger(logger, "get_coinm_order_book")
        msg = (_blank("symbol", symbol)
            or _in("limit", limit, _BOOK_LIMITS))
        if msg:
            return _err(CoinmOrderBookResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/depth", "NONE", "order_book", symbol=symbol, limit=limit)
            tlog.success()
            return CoinmOrderBookResult(success=True, statusCode=200, data=CoinmOrderBookData(**data))
        except Exception as exc:
            return _handle_request_exc(CoinmOrderBookResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_price_ticker",
        description=(
            "Returns the latest price for one COIN-M futures symbol, all symbols of a pair, or all symbols "
            "when both are omitted. Symbol and pair cannot be sent together; request weight is 1 for a single "
            "symbol and 2 when symbol is omitted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_price_ticker(
        symbol: str | None = Field(default=None, description="Symbol, e.g. BTCUSD_PERP. Cannot be combined with pair. Omit both to return all symbols."),
        pair: str | None = Field(default=None, description="Pair, e.g. BTCUSD. Cannot be combined with symbol. Omit both to return all symbols."),
    ) -> CoinmPriceTickerResult:
        tlog = ToolLogger(logger, "get_coinm_price_ticker")
        if symbol and pair:
            return _err(CoinmPriceTickerResult, tlog, "VALIDATION_ERROR", "symbol and pair cannot be sent together", 400)
        try:
            data = service.call("coinm", "/dapi/v1/ticker/price", "NONE", "symbol_price_ticker", symbol=symbol, pair=pair)
            tlog.success()
            return CoinmPriceTickerResult(success=True, statusCode=200, data=CoinmPriceTickerData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmPriceTickerResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_server_time",
        description=(
            "Tests connectivity to the COIN-M REST API and returns the current server time in milliseconds."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_server_time(
    ) -> CoinmServerTimeResult:
        tlog = ToolLogger(logger, "get_coinm_server_time")
        try:
            data = service.call("coinm", "/dapi/v1/time", "NONE", "check_server_time")
            tlog.success()
            return CoinmServerTimeResult(success=True, statusCode=200, data=CoinmServerTimeData(**data))
        except Exception as exc:
            return _handle_request_exc(CoinmServerTimeResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_top_trader_account_ratio",
        description=(
            "Returns the long/short account ratio history of top traders (top 20% by margin balance) for a "
            "COIN-M pair, each account counted once. Only the latest 30 days are available; without startTime "
            "and endTime the most recent data is returned."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_top_trader_account_ratio(
        pair: str = Field(description="COIN-M pair, e.g. BTCUSD."),
        period: str = Field(description="Period of each data point: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h or 1d."),
        contract_type: str | None = Field(default=None, description="Contract type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER. Omit to aggregate across all contract types."),
        limit: int = Field(default=30, description="Maximum number of records to return, up to 500. Defaults to 30."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
    ) -> CoinmTopTraderAccountRatioResult:
        tlog = ToolLogger(logger, "get_coinm_top_trader_account_ratio")
        msg = (_blank("pair", pair)
            or _in("period", period, _PERIODS)
            or _in("contract_type", contract_type, _CONTRACT_TYPES)
            or _max("limit", limit, 500))
        if msg:
            return _err(CoinmTopTraderAccountRatioResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/futures/data/topLongShortAccountRatio", "NONE", "top_trader_long_short_ratio_accounts", pair=pair, period=period, contract_type=contract_type, limit=limit, start_time=start_time, end_time=end_time)
            tlog.success()
            return CoinmTopTraderAccountRatioResult(success=True, statusCode=200, data=CoinmTopTraderAccountRatioData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmTopTraderAccountRatioResult, tlog, exc)

    @mcp.tool(
        name="get_coinm_top_trader_position_ratio",
        description=(
            "Returns the long/short position ratio history of top traders (top 20% by margin balance) for a "
            "COIN-M pair, based on open positions. Only the latest 30 days are available; without startTime "
            "and endTime the most recent data is returned."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_coinm_top_trader_position_ratio(
        pair: str = Field(description="COIN-M pair, e.g. BTCUSD."),
        period: str = Field(description="Period of each data point: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h or 1d."),
        contract_type: str | None = Field(default=None, description="Contract type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER. Omit to aggregate across all contract types."),
        limit: int = Field(default=30, description="Maximum number of records to return, up to 500. Defaults to 30."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
    ) -> CoinmTopTraderPositionRatioResult:
        tlog = ToolLogger(logger, "get_coinm_top_trader_position_ratio")
        msg = (_blank("pair", pair)
            or _in("period", period, _PERIODS)
            or _in("contract_type", contract_type, _CONTRACT_TYPES)
            or _max("limit", limit, 500))
        if msg:
            return _err(CoinmTopTraderPositionRatioResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/futures/data/topLongShortPositionRatio", "NONE", "top_trader_long_short_ratio_positions", pair=pair, period=period, contract_type=contract_type, limit=limit, start_time=start_time, end_time=end_time)
            tlog.success()
            return CoinmTopTraderPositionRatioResult(success=True, statusCode=200, data=CoinmTopTraderPositionRatioData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmTopTraderPositionRatioResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_agg_trades",
        description=(
            "Returns compressed aggregate trades for a COIN-M symbol, where fills within 100ms at the same "
            "price and side are combined (market trades only). Only the past 48 hours can be queried, "
            "startTime to endTime must span less than 1 hour, and sending fromId together with a time range "
            "can time out, so send one or the other. Request weight is 20."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_agg_trades(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP."),
        from_id: int | None = Field(default=None, description="Aggregate trade ID to start from, inclusive. Omit to use the most recent trades."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch, inclusive."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch, inclusive."),
        limit: int = Field(default=500, description="Maximum number of records to return, up to 1000. Defaults to 500."),
    ) -> CoinmAggTradesListResult:
        tlog = ToolLogger(logger, "list_coinm_agg_trades")
        msg = (_blank("symbol", symbol)
            or _max("limit", limit, 1000))
        if msg:
            return _err(CoinmAggTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/aggTrades", "NONE", "compressed_aggregate_trades_list", symbol=symbol, from_id=from_id, start_time=start_time, end_time=end_time, limit=limit)
            tlog.success()
            return CoinmAggTradesListResult(success=True, statusCode=200, data=CoinmAggTradesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmAggTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_basis",
        description=(
            "Returns the futures basis history (index price, futures price, basis, basis rate and annualized "
            "basis rate) for a COIN-M pair and contract type. Only the latest 30 days are available; without "
            "startTime and endTime the most recent data is returned."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_basis(
        pair: str = Field(description="COIN-M pair, e.g. BTCUSD."),
        contract_type: str = Field(description="Contract type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER."),
        period: str = Field(description="Period of each data point: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h or 1d."),
        limit: int = Field(default=30, description="Maximum number of records to return, up to 500. Defaults to 30."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
    ) -> CoinmBasisListResult:
        tlog = ToolLogger(logger, "list_coinm_basis")
        msg = (_blank("pair", pair)
            or _in("contract_type", contract_type, _CONTRACT_TYPES)
            or _in("period", period, _PERIODS)
            or _max("limit", limit, 500))
        if msg:
            return _err(CoinmBasisListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/futures/data/basis", "NONE", "basis", pair=pair, contract_type=contract_type, period=period, limit=limit, start_time=start_time, end_time=end_time)
            tlog.success()
            return CoinmBasisListResult(success=True, statusCode=200, data=CoinmBasisListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmBasisListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_continuous_klines",
        description=(
            "Returns kline/candlestick bars for a COIN-M pair and contract type. Each kline is a 12-element "
            "array: [open time, open, high, low, close, volume, close time, base asset volume, number of "
            "trades, taker buy volume, taker buy base asset volume, unused]. The startTime to endTime span "
            "can be at most 200 days; with no times given the most recent bars are returned. Request weight "
            "is 1-10 depending on limit."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_continuous_klines(
        pair: str = Field(description="Pair, e.g. BTCUSD (UM pairs are also accepted after the CM migration)."),
        contract_type: str = Field(description="Contract type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER."),
        interval: str = Field(description="Kline interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w or 1M."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
        limit: int = Field(default=500, description="Maximum number of records to return, up to 1500. Defaults to 500."),
    ) -> CoinmContinuousKlinesListResult:
        tlog = ToolLogger(logger, "list_coinm_continuous_klines")
        msg = (_blank("pair", pair)
            or _in("contract_type", contract_type, _CONTRACT_TYPES)
            or _in("interval", interval, _INTERVALS)
            or _max("limit", limit, 1500))
        if msg:
            return _err(CoinmContinuousKlinesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/continuousKlines", "NONE", "continuous_contract_kline_candlestick_data", pair=pair, contract_type=contract_type, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            tlog.success()
            return CoinmContinuousKlinesListResult(success=True, statusCode=200, data=CoinmContinuousKlinesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmContinuousKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_funding_rate_history",
        description=(
            "Returns the funding rate history of a COIN-M perpetual symbol; an empty list is returned for "
            "delivery symbols."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_funding_rate_history(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch, inclusive. Omit for no lower bound."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch, inclusive. Omit for no upper bound."),
        limit: int = Field(default=100, description="Maximum number of records to return, up to 1000. Defaults to 100."),
    ) -> CoinmFundingRateHistoryListResult:
        tlog = ToolLogger(logger, "list_coinm_funding_rate_history")
        msg = (_blank("symbol", symbol)
            or _max("limit", limit, 1000))
        if msg:
            return _err(CoinmFundingRateHistoryListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/fundingRate", "NONE", "get_funding_rate_history_of_perpetual_futures", symbol=symbol, start_time=start_time, end_time=end_time, limit=limit)
            tlog.success()
            return CoinmFundingRateHistoryListResult(success=True, statusCode=200, data=CoinmFundingRateHistoryListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmFundingRateHistoryListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_historical_trades",
        description=(
            "Returns older market trades for a COIN-M symbol from the last month, starting at fromId or at "
            "the most recent trades. Reads market data with the connected Binance API key (no signature); "
            "request weight is 200."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_historical_trades(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP."),
        limit: int = Field(default=100, description="Maximum number of records to return, up to 500. Defaults to 100."),
        from_id: int | None = Field(default=None, description="Trade ID to fetch from. Omit to get the most recent trades."),
    ) -> CoinmHistoricalTradesListResult:
        tlog = ToolLogger(logger, "list_coinm_historical_trades")
        msg = (_blank("symbol", symbol)
            or _max("limit", limit, 500))
        if msg:
            return _err(CoinmHistoricalTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/historicalTrades", "MARKET_DATA", "old_trades_lookup", symbol=symbol, limit=limit, from_id=from_id)
            tlog.success()
            return CoinmHistoricalTradesListResult(success=True, statusCode=200, data=CoinmHistoricalTradesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmHistoricalTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_index_price_klines",
        description=(
            "Returns kline/candlestick bars for the index price of a COIN-M pair. Each kline is a 12-element "
            "array: [open time, open, high, low, close, unused, close time, unused, number of basic data, "
            "unused, unused, unused]. The startTime to endTime span can be at most 200 days; with no times "
            "given the most recent bars are returned. Request weight is 1-10 depending on limit."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_index_price_klines(
        pair: str = Field(description="Pair, e.g. BTCUSD (UM pairs are also accepted after the CM migration)."),
        interval: str = Field(description="Kline interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w or 1M."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
        limit: int = Field(default=500, description="Maximum number of records to return, up to 1500. Defaults to 500."),
    ) -> CoinmIndexPriceKlinesListResult:
        tlog = ToolLogger(logger, "list_coinm_index_price_klines")
        msg = (_blank("pair", pair)
            or _in("interval", interval, _INTERVALS)
            or _max("limit", limit, 1500))
        if msg:
            return _err(CoinmIndexPriceKlinesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/indexPriceKlines", "NONE", "index_price_kline_candlestick_data", pair=pair, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            tlog.success()
            return CoinmIndexPriceKlinesListResult(success=True, statusCode=200, data=CoinmIndexPriceKlinesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmIndexPriceKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_klines",
        description=(
            "Returns kline/candlestick bars for a COIN-M futures symbol. Each kline is a 12-element array: "
            "[open time, open, high, low, close, volume, close time, base asset volume, number of trades, "
            "taker buy volume, taker buy base asset volume, unused]. The startTime to endTime span can be at "
            "most 200 days; with no times given the most recent bars are returned. Request weight is 1-10 "
            "depending on limit."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_klines(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP (UM symbols are also accepted after the CM migration)."),
        interval: str = Field(description="Kline interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w or 1M."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
        limit: int = Field(default=500, description="Maximum number of records to return, up to 1500. Defaults to 500."),
    ) -> CoinmKlinesListResult:
        tlog = ToolLogger(logger, "list_coinm_klines")
        msg = (_blank("symbol", symbol)
            or _in("interval", interval, _INTERVALS)
            or _max("limit", limit, 1500))
        if msg:
            return _err(CoinmKlinesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/klines", "NONE", "kline_candlestick_data", symbol=symbol, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            tlog.success()
            return CoinmKlinesListResult(success=True, statusCode=200, data=CoinmKlinesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_mark_price_klines",
        description=(
            "Returns kline/candlestick bars for the mark price of a COIN-M futures symbol. Each kline is a "
            "12-element array: [open time, open, high, low, close, unused, close time, unused, number of "
            "basic data, unused, unused, unused]. The startTime to endTime span can be at most 200 days; with "
            "no times given the most recent bars are returned. Request weight is 1-10 depending on limit."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_mark_price_klines(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP (UM symbols are also accepted after the CM migration)."),
        interval: str = Field(description="Kline interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w or 1M."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
        limit: int = Field(default=500, description="Maximum number of records to return, up to 1500. Defaults to 500."),
    ) -> CoinmMarkPriceKlinesListResult:
        tlog = ToolLogger(logger, "list_coinm_mark_price_klines")
        msg = (_blank("symbol", symbol)
            or _in("interval", interval, _INTERVALS)
            or _max("limit", limit, 1500))
        if msg:
            return _err(CoinmMarkPriceKlinesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/markPriceKlines", "NONE", "mark_price_kline_candlestick_data", symbol=symbol, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            tlog.success()
            return CoinmMarkPriceKlinesListResult(success=True, statusCode=200, data=CoinmMarkPriceKlinesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmMarkPriceKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_open_interest_stats",
        description=(
            "Returns open interest statistics (in contracts and base asset) for a COIN-M pair at the chosen "
            "period. Only the latest 30 days are available; without startTime and endTime the most recent "
            "data is returned."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_open_interest_stats(
        pair: str = Field(description="COIN-M pair, e.g. BTCUSD."),
        period: str = Field(description="Period of each data point: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h or 1d."),
        contract_type: str | None = Field(default=None, description="Contract type: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER. Omit to aggregate across all contract types."),
        limit: int = Field(default=30, description="Maximum number of records to return, up to 500. Defaults to 30."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
    ) -> CoinmOpenInterestStatsListResult:
        tlog = ToolLogger(logger, "list_coinm_open_interest_stats")
        msg = (_blank("pair", pair)
            or _in("contract_type", contract_type, _CONTRACT_TYPES)
            or _in("period", period, _PERIODS)
            or _max("limit", limit, 500))
        if msg:
            return _err(CoinmOpenInterestStatsListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/futures/data/openInterestHist", "NONE", "open_interest_statistics", pair=pair, contract_type=contract_type, period=period, limit=limit, start_time=start_time, end_time=end_time)
            tlog.success()
            return CoinmOpenInterestStatsListResult(success=True, statusCode=200, data=CoinmOpenInterestStatsListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmOpenInterestStatsListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_premium_index_klines",
        description=(
            "Returns premium index kline bars for a COIN-M futures symbol. Each kline is a 12-element array: "
            "[open time, open, high, low, close, unused, close time, unused, unused, unused, unused, unused]. "
            "Without startTime and endTime the most recent bars are returned; request weight is 1-10 "
            "depending on limit."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_premium_index_klines(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP (UM symbols are also accepted after the CM migration)."),
        interval: str = Field(description="Kline interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w or 1M."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
        limit: int = Field(default=500, description="Maximum number of records to return, up to 1500. Defaults to 500."),
    ) -> CoinmPremiumIndexKlinesListResult:
        tlog = ToolLogger(logger, "list_coinm_premium_index_klines")
        msg = (_blank("symbol", symbol)
            or _in("interval", interval, _INTERVALS)
            or _max("limit", limit, 1500))
        if msg:
            return _err(CoinmPremiumIndexKlinesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/premiumIndexKlines", "NONE", "premium_index_kline_data", symbol=symbol, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            tlog.success()
            return CoinmPremiumIndexKlinesListResult(success=True, statusCode=200, data=CoinmPremiumIndexKlinesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmPremiumIndexKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_recent_trades",
        description=(
            "Returns recent market trades for a COIN-M futures symbol (insurance fund and ADL trades are "
            "excluded)."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_recent_trades(
        symbol: str = Field(description="COIN-M futures symbol, e.g. BTCUSD_PERP."),
        limit: int = Field(default=500, description="Maximum number of records to return, up to 1000. Defaults to 500."),
    ) -> CoinmRecentTradesListResult:
        tlog = ToolLogger(logger, "list_coinm_recent_trades")
        msg = (_blank("symbol", symbol)
            or _max("limit", limit, 1000))
        if msg:
            return _err(CoinmRecentTradesListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/dapi/v1/trades", "NONE", "recent_trades_list", symbol=symbol, limit=limit)
            tlog.success()
            return CoinmRecentTradesListResult(success=True, statusCode=200, data=CoinmRecentTradesListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmRecentTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_coinm_taker_buy_sell_volume",
        description=(
            "Returns taker buy and sell volume per period for a COIN-M pair and contract type. Only the "
            "latest 30 days are available; without startTime and endTime the most recent data is returned."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_coinm_taker_buy_sell_volume(
        pair: str = Field(description="COIN-M pair, e.g. BTCUSD."),
        contract_type: str = Field(description="Contract type: ALL, PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER."),
        period: str = Field(description="Period of each data point: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h or 1d."),
        limit: int = Field(default=30, description="Maximum number of records to return, up to 500. Defaults to 30."),
        start_time: int | None = Field(default=None, description="Start of the range in milliseconds since epoch. Omit to use the most recent data."),
        end_time: int | None = Field(default=None, description="End of the range in milliseconds since epoch. Omit to use the most recent data."),
    ) -> CoinmTakerBuySellVolumeListResult:
        tlog = ToolLogger(logger, "list_coinm_taker_buy_sell_volume")
        msg = (_blank("pair", pair)
            or _in("contract_type", contract_type, _CONTRACT_TYPES_ALL)
            or _in("period", period, _PERIODS)
            or _max("limit", limit, 500))
        if msg:
            return _err(CoinmTakerBuySellVolumeListResult, tlog, "VALIDATION_ERROR", msg, 400)
        try:
            data = service.call("coinm", "/futures/data/takerBuySellVol", "NONE", "taker_buy_sell_volume", pair=pair, contract_type=contract_type, period=period, limit=limit, start_time=start_time, end_time=end_time)
            tlog.success()
            return CoinmTakerBuySellVolumeListResult(success=True, statusCode=200, data=CoinmTakerBuySellVolumeListData(count=len(data), items=data))
        except Exception as exc:
            return _handle_request_exc(CoinmTakerBuySellVolumeListResult, tlog, exc)

    @mcp.tool(
        name="ping_coinm",
        description=(
            "Tests connectivity to the COIN-M Futures REST API and returns an empty payload on success."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def ping_coinm(
    ) -> PingCoinmResult:
        tlog = ToolLogger(logger, "ping_coinm")
        try:
            data = service.call("coinm", "/dapi/v1/ping", "NONE", "test_connectivity")
            tlog.success()
            return PingCoinmResult(success=True, statusCode=200, data=PingCoinmData())
        except Exception as exc:
            return _handle_request_exc(PingCoinmResult, tlog, exc)
