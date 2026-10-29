"""Usdm market group: get_usdm_24hr_ticker, get_usdm_asset_index, get_usdm_book_ticker, get_usdm_composite_index_info, get_usdm_exchange_info, get_usdm_funding_rate_info, get_usdm_index_constituents, get_usdm_insurance_fund_balance, get_usdm_long_short_ratio, get_usdm_mark_price, get_usdm_open_interest, get_usdm_order_book, get_usdm_price_ticker, get_usdm_rpi_order_book, get_usdm_server_time, get_usdm_symbol_adl_risk, get_usdm_top_trader_account_ratio, get_usdm_top_trader_position_ratio, get_usdm_trading_schedule, list_usdm_agg_trades, list_usdm_basis, list_usdm_continuous_klines, list_usdm_delivery_prices, list_usdm_funding_rate_history, list_usdm_historical_trades, list_usdm_index_price_klines, list_usdm_klines, list_usdm_mark_price_klines, list_usdm_open_interest_stats, list_usdm_premium_index_klines, list_usdm_recent_trades, list_usdm_taker_buy_sell_volume, ping_usdm"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.usdm_market import (
    PingUsdmData,
    PingUsdmResult,
    Usdm24hrTickerData,
    Usdm24hrTickerResult,
    UsdmAggTradesListData,
    UsdmAggTradesListResult,
    UsdmAssetIndexData,
    UsdmAssetIndexResult,
    UsdmBasisListData,
    UsdmBasisListResult,
    UsdmBookTickerData,
    UsdmBookTickerResult,
    UsdmCompositeIndexInfoData,
    UsdmCompositeIndexInfoResult,
    UsdmContinuousKlinesListData,
    UsdmContinuousKlinesListResult,
    UsdmDeliveryPricesListData,
    UsdmDeliveryPricesListResult,
    UsdmExchangeInfoData,
    UsdmExchangeInfoResult,
    UsdmFundingRateHistoryListData,
    UsdmFundingRateHistoryListResult,
    UsdmFundingRateInfoData,
    UsdmFundingRateInfoResult,
    UsdmHistoricalTradesListData,
    UsdmHistoricalTradesListResult,
    UsdmIndexConstituentsData,
    UsdmIndexConstituentsResult,
    UsdmIndexPriceKlinesListData,
    UsdmIndexPriceKlinesListResult,
    UsdmInsuranceFundBalanceData,
    UsdmInsuranceFundBalanceResult,
    UsdmKlinesListData,
    UsdmKlinesListResult,
    UsdmLongShortRatioData,
    UsdmLongShortRatioResult,
    UsdmMarkPriceData,
    UsdmMarkPriceKlinesListData,
    UsdmMarkPriceKlinesListResult,
    UsdmMarkPriceResult,
    UsdmOpenInterestData,
    UsdmOpenInterestResult,
    UsdmOpenInterestStatsListData,
    UsdmOpenInterestStatsListResult,
    UsdmOrderBookData,
    UsdmOrderBookResult,
    UsdmPremiumIndexKlinesListData,
    UsdmPremiumIndexKlinesListResult,
    UsdmPriceTickerData,
    UsdmPriceTickerResult,
    UsdmRecentTradesListData,
    UsdmRecentTradesListResult,
    UsdmRpiOrderBookData,
    UsdmRpiOrderBookResult,
    UsdmServerTimeData,
    UsdmServerTimeResult,
    UsdmSymbolAdlRiskData,
    UsdmSymbolAdlRiskResult,
    UsdmTakerBuySellVolumeListData,
    UsdmTakerBuySellVolumeListResult,
    UsdmTopTraderAccountRatioData,
    UsdmTopTraderAccountRatioResult,
    UsdmTopTraderPositionRatioData,
    UsdmTopTraderPositionRatioResult,
    UsdmTradingScheduleData,
    UsdmTradingScheduleResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("binance-mcp.tools.usdm_market")


def register_usdm_market_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_usdm_24hr_ticker",
        description=(
            "Returns 24-hour rolling window price change statistics for one USDⓈ-M futures symbol, or a "
            "list for every symbol when symbol is omitted. Weight is 1 for a single symbol and 40 when "
            "symbol is omitted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_24hr_ticker(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BTCUSDT. Omit to return tickers for all symbols as a list."),
    ) -> Usdm24hrTickerResult:
        tlog = ToolLogger(logger, "get_usdm_24hr_ticker")
        try:
            data = service.call("usdm", "/fapi/v1/ticker/24hr", "NONE", "ticker24hr_price_change_statistics", symbol=symbol)
            payload = Usdm24hrTickerData(count=len(data), items=data) if isinstance(data, list) else Usdm24hrTickerData(**data)
            tlog.success()
            return Usdm24hrTickerResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(Usdm24hrTickerResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_asset_index",
        description=(
            "Returns the asset index price for Multi-Assets mode for one asset pair, or a list for all "
            "pairs when symbol is omitted. The response also includes COIN-M settlement-asset price index "
            "entries such as BTCUSD, ETHUSD and BNBUSD. Weight is 1 with a symbol and 10 without."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_asset_index(
        symbol: str | None = Field(default=None, description="Asset pair symbol. Omit to return all asset indexes as a list."),
    ) -> UsdmAssetIndexResult:
        tlog = ToolLogger(logger, "get_usdm_asset_index")
        try:
            data = service.call("usdm", "/fapi/v1/assetIndex", "NONE", "asset_index", symbol=symbol)
            payload = UsdmAssetIndexData(count=len(data), items=data) if isinstance(data, list) else UsdmAssetIndexData(**data)
            tlog.success()
            return UsdmAssetIndexResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmAssetIndexResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_book_ticker",
        description=(
            "Returns the best bid and ask price and quantity for one symbol, or a list for all symbols "
            "when symbol is omitted. Retail Price Improvement (RPI) orders are not visible and are "
            "excluded. Weight is 2 for a single symbol and 5 when symbol is omitted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_book_ticker(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BTCUSDT. Omit to return book tickers for all symbols as a list."),
    ) -> UsdmBookTickerResult:
        tlog = ToolLogger(logger, "get_usdm_book_ticker")
        try:
            data = service.call("usdm", "/fapi/v1/ticker/bookTicker", "NONE", "symbol_order_book_ticker", symbol=symbol)
            payload = UsdmBookTickerData(count=len(data), items=data) if isinstance(data, list) else UsdmBookTickerData(**data)
            tlog.success()
            return UsdmBookTickerResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmBookTickerResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_composite_index_info",
        description=(
            "Returns composite index symbol information, including the base and quote asset weights of "
            "each component, for one symbol or a list when symbol is omitted. Applies only to composite "
            "index symbols."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_composite_index_info(
        symbol: str | None = Field(default=None, description="Composite index symbol. Omit to return all composite index symbols as a list."),
    ) -> UsdmCompositeIndexInfoResult:
        tlog = ToolLogger(logger, "get_usdm_composite_index_info")
        try:
            data = service.call("usdm", "/fapi/v1/indexInfo", "NONE", "composite_index_symbol_information", symbol=symbol)
            payload = UsdmCompositeIndexInfoData(count=len(data), items=data) if isinstance(data, list) else UsdmCompositeIndexInfoData(**data)
            tlog.success()
            return UsdmCompositeIndexInfoResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmCompositeIndexInfoResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_exchange_info",
        description=(
            "Returns current exchange trading rules, rate limits and symbol information (contract type, "
            "status, precisions, filters, order types) for USDⓈ-M futures. The response covers every "
            "symbol and is large."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_exchange_info() -> UsdmExchangeInfoResult:
        tlog = ToolLogger(logger, "get_usdm_exchange_info")
        try:
            data = service.call("usdm", "/fapi/v1/exchangeInfo", "NONE", "exchange_information")
            payload = UsdmExchangeInfoData(**data)
            tlog.success()
            return UsdmExchangeInfoResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmExchangeInfoResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_funding_rate_info",
        description=(
            "Returns funding rate cap, floor and interval hours for symbols that had a funding rate cap, "
            "floor or funding interval adjustment; other symbols are not included. Shares the 500/5min/IP "
            "rate limit with list_usdm_funding_rate_history."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_funding_rate_info() -> UsdmFundingRateInfoResult:
        tlog = ToolLogger(logger, "get_usdm_funding_rate_info")
        try:
            data = service.call("usdm", "/fapi/v1/fundingInfo", "NONE", "get_funding_rate_info")
            payload = UsdmFundingRateInfoData(count=len(data), items=data)
            tlog.success()
            return UsdmFundingRateInfoResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmFundingRateInfoResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_index_constituents",
        description=(
            "Returns the constituents (exchange, symbol, price and weight) of the index price for a "
            "symbol. Prices from constituents of TradFi perpetuals are hidden and shown as -1."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_index_constituents(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
    ) -> UsdmIndexConstituentsResult:
        tlog = ToolLogger(logger, "get_usdm_index_constituents")
        if not symbol.strip():
            return _err(UsdmIndexConstituentsResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        try:
            data = service.call("usdm", "/fapi/v1/constituents", "NONE", "query_index_price_constituents", symbol=symbol)
            payload = UsdmIndexConstituentsData(**data)
            tlog.success()
            return UsdmIndexConstituentsResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmIndexConstituentsResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_insurance_fund_balance",
        description=(
            "Returns the insurance fund balance snapshot: the symbols each fund covers and its margin "
            "balance per asset. A single fund object is returned when symbol is given, otherwise a list "
            "of all funds."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_insurance_fund_balance(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BTCUSDT. Omit to return all insurance funds as a list."),
    ) -> UsdmInsuranceFundBalanceResult:
        tlog = ToolLogger(logger, "get_usdm_insurance_fund_balance")
        try:
            data = service.call("usdm", "/fapi/v1/insuranceBalance", "NONE", "query_insurance_fund_balance_snapshot", symbol=symbol)
            payload = UsdmInsuranceFundBalanceData(count=len(data), items=data) if isinstance(data, list) else UsdmInsuranceFundBalanceData(**data)
            tlog.success()
            return UsdmInsuranceFundBalanceResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmInsuranceFundBalanceResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_long_short_ratio",
        description=(
            "Returns the long/short account ratio of all traders for a symbol over a statistics period. "
            "The most recent data is returned when start_time and end_time are omitted; only the latest "
            "30 days are available. IP rate limit is 1000 requests/5min."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_long_short_ratio(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        period: str = Field(description="Statistics period. One of 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d."),
        limit: int = Field(default=30, description="Number of records to return (default 30, maximum 500)."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
    ) -> UsdmLongShortRatioResult:
        tlog = ToolLogger(logger, "get_usdm_long_short_ratio")
        if not symbol.strip():
            return _err(UsdmLongShortRatioResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if not period.strip():
            return _err(UsdmLongShortRatioResult, tlog, "VALIDATION_ERROR", "period must not be empty", 400)
        if period not in ("5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"):
            return _err(UsdmLongShortRatioResult, tlog, "VALIDATION_ERROR", "period must be one of: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d", 400)
        if limit > 500:
            return _err(UsdmLongShortRatioResult, tlog, "VALIDATION_ERROR", "limit must be at most 500", 400)
        try:
            data = service.call("usdm", "/futures/data/globalLongShortAccountRatio", "NONE", "long_short_ratio", symbol=symbol, period=period, limit=limit, start_time=start_time, end_time=end_time)
            payload = UsdmLongShortRatioData(count=len(data), items=data)
            tlog.success()
            return UsdmLongShortRatioResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmLongShortRatioResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_mark_price",
        description=(
            "Returns the mark price, index price, latest funding rate and next funding time for one "
            "symbol, or a list for all symbols when symbol is omitted. Weight is 1 with a symbol and 10 "
            "without."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_mark_price(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BTCUSDT. Omit to return mark prices for all symbols as a list."),
    ) -> UsdmMarkPriceResult:
        tlog = ToolLogger(logger, "get_usdm_mark_price")
        try:
            data = service.call("usdm", "/fapi/v1/premiumIndex", "NONE", "mark_price", symbol=symbol)
            payload = UsdmMarkPriceData(count=len(data), items=data) if isinstance(data, list) else UsdmMarkPriceData(**data)
            tlog.success()
            return UsdmMarkPriceResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmMarkPriceResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_open_interest",
        description=(
            "Returns the present open interest of a symbol."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_open_interest(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
    ) -> UsdmOpenInterestResult:
        tlog = ToolLogger(logger, "get_usdm_open_interest")
        if not symbol.strip():
            return _err(UsdmOpenInterestResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        try:
            data = service.call("usdm", "/fapi/v1/openInterest", "NONE", "open_interest", symbol=symbol)
            payload = UsdmOpenInterestData(**data)
            tlog.success()
            return UsdmOpenInterestResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmOpenInterestResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_order_book",
        description=(
            "Returns the order book for a symbol as bids and asks, each entry a [price, quantity] pair of "
            "strings, excluding Retail Price Improvement (RPI) orders. Weight depends on limit: 2 for 5 "
            "to 50, 5 for 100, 10 for 500 and 20 for 1000."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_order_book(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        limit: int = Field(default=500, description="Number of price levels per side. Valid values: 5, 10, 20, 50, 100, 500, 1000 (default 500)."),
    ) -> UsdmOrderBookResult:
        tlog = ToolLogger(logger, "get_usdm_order_book")
        if not symbol.strip():
            return _err(UsdmOrderBookResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if limit not in (5, 10, 20, 50, 100, 500, 1000):
            return _err(UsdmOrderBookResult, tlog, "VALIDATION_ERROR", "limit must be one of: 5, 10, 20, 50, 100, 500, 1000", 400)
        try:
            data = service.call("usdm", "/fapi/v1/depth", "NONE", "order_book", symbol=symbol, limit=limit)
            payload = UsdmOrderBookData(**data)
            tlog.success()
            return UsdmOrderBookResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmOrderBookResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_price_ticker",
        description=(
            "Returns the latest price for one symbol, or a list for all symbols when symbol is omitted. "
            "Weight is 1 for a single symbol and 2 when symbol is omitted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_price_ticker(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BTCUSDT. Omit to return prices for all symbols as a list."),
    ) -> UsdmPriceTickerResult:
        tlog = ToolLogger(logger, "get_usdm_price_ticker")
        try:
            data = service.call("usdm", "/fapi/v2/ticker/price", "NONE", "symbol_price_ticker_v2", symbol=symbol)
            payload = UsdmPriceTickerData(count=len(data), items=data) if isinstance(data, list) else UsdmPriceTickerData(**data)
            tlog.success()
            return UsdmPriceTickerResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmPriceTickerResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_rpi_order_book",
        description=(
            "Returns the order book for a symbol as bids and asks, each entry a [price, quantity] pair of "
            "strings, including aggregated Retail Price Improvement (RPI) orders. Crossed price levels "
            "are hidden. Weight is 20."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_rpi_order_book(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        limit: int = Field(default=1000, description="Number of price levels per side. Valid value: 1000 (default 1000)."),
    ) -> UsdmRpiOrderBookResult:
        tlog = ToolLogger(logger, "get_usdm_rpi_order_book")
        if not symbol.strip():
            return _err(UsdmRpiOrderBookResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if limit not in (1000,):
            return _err(UsdmRpiOrderBookResult, tlog, "VALIDATION_ERROR", "limit must be one of: 1000", 400)
        try:
            data = service.call("usdm", "/fapi/v1/rpiDepth", "NONE", "rpi_order_book", symbol=symbol, limit=limit)
            payload = UsdmRpiOrderBookData(**data)
            tlog.success()
            return UsdmRpiOrderBookResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmRpiOrderBookResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_server_time",
        description=(
            "Tests connectivity to the REST API and returns the current server time in milliseconds."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_server_time() -> UsdmServerTimeResult:
        tlog = ToolLogger(logger, "get_usdm_server_time")
        try:
            data = service.call("usdm", "/fapi/v1/time", "NONE", "check_server_time")
            payload = UsdmServerTimeData(**data)
            tlog.success()
            return UsdmServerTimeResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmServerTimeResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_symbol_adl_risk",
        description=(
            "Returns the symbol-level ADL (auto-deleveraging) risk rating (high, medium or low), updated "
            "every 30 minutes, for one symbol or a list for all symbols when symbol is omitted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_symbol_adl_risk(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BTCUSDT. Omit to return ratings for all symbols as a list."),
    ) -> UsdmSymbolAdlRiskResult:
        tlog = ToolLogger(logger, "get_usdm_symbol_adl_risk")
        try:
            data = service.call("usdm", "/fapi/v1/symbolAdlRisk", "NONE", "adl_risk", symbol=symbol)
            payload = UsdmSymbolAdlRiskData(count=len(data), items=data) if isinstance(data, list) else UsdmSymbolAdlRiskData(**data)
            tlog.success()
            return UsdmSymbolAdlRiskResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmSymbolAdlRiskResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_top_trader_account_ratio",
        description=(
            "Returns the net long/short account proportion of the top 20% of users by margin balance for "
            "a symbol, counting each account once. Requires a Binance API key but no signature. The most "
            "recent data is returned when start_time and end_time are omitted; only the latest 30 days "
            "are available. IP rate limit is 1000 requests/5min."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_top_trader_account_ratio(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        period: str = Field(description="Statistics period. One of 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d."),
        limit: int = Field(default=30, description="Number of records to return (default 30, maximum 500)."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
    ) -> UsdmTopTraderAccountRatioResult:
        tlog = ToolLogger(logger, "get_usdm_top_trader_account_ratio")
        if not symbol.strip():
            return _err(UsdmTopTraderAccountRatioResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if not period.strip():
            return _err(UsdmTopTraderAccountRatioResult, tlog, "VALIDATION_ERROR", "period must not be empty", 400)
        if period not in ("5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"):
            return _err(UsdmTopTraderAccountRatioResult, tlog, "VALIDATION_ERROR", "period must be one of: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d", 400)
        if limit > 500:
            return _err(UsdmTopTraderAccountRatioResult, tlog, "VALIDATION_ERROR", "limit must be at most 500", 400)
        try:
            data = service.call("usdm", "/futures/data/topLongShortAccountRatio", "MARKET_DATA", "top_trader_long_short_ratio_accounts", symbol=symbol, period=period, limit=limit, start_time=start_time, end_time=end_time)
            payload = UsdmTopTraderAccountRatioData(count=len(data), items=data)
            tlog.success()
            return UsdmTopTraderAccountRatioResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmTopTraderAccountRatioResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_top_trader_position_ratio",
        description=(
            "Returns the net long/short position proportion of the top 20% of users by margin balance for "
            "a symbol. Requires a Binance API key but no signature. The most recent data is returned when "
            "start_time and end_time are omitted; only the latest 30 days are available. IP rate limit is "
            "1000 requests/5min."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_top_trader_position_ratio(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        period: str = Field(description="Statistics period. One of 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d."),
        limit: int = Field(default=30, description="Number of records to return (default 30, maximum 500)."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
    ) -> UsdmTopTraderPositionRatioResult:
        tlog = ToolLogger(logger, "get_usdm_top_trader_position_ratio")
        if not symbol.strip():
            return _err(UsdmTopTraderPositionRatioResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if not period.strip():
            return _err(UsdmTopTraderPositionRatioResult, tlog, "VALIDATION_ERROR", "period must not be empty", 400)
        if period not in ("5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"):
            return _err(UsdmTopTraderPositionRatioResult, tlog, "VALIDATION_ERROR", "period must be one of: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d", 400)
        if limit > 500:
            return _err(UsdmTopTraderPositionRatioResult, tlog, "VALIDATION_ERROR", "limit must be at most 500", 400)
        try:
            data = service.call("usdm", "/futures/data/topLongShortPositionRatio", "MARKET_DATA", "top_trader_long_short_ratio_positions", symbol=symbol, period=period, limit=limit, start_time=start_time, end_time=end_time)
            payload = UsdmTopTraderPositionRatioData(count=len(data), items=data)
            tlog.success()
            return UsdmTopTraderPositionRatioResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmTopTraderPositionRatioResult, tlog, exc)

    @mcp.tool(
        name="get_usdm_trading_schedule",
        description=(
            "Returns trading session schedules (start time, end time and session type) for the underlying "
            "assets of TradFi perpetuals across the U.S., Korean, Hong Kong and China equity markets, the "
            "commodity market and the FX market. Covers one week backward and one week forward from the "
            "day before the query time."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_usdm_trading_schedule() -> UsdmTradingScheduleResult:
        tlog = ToolLogger(logger, "get_usdm_trading_schedule")
        try:
            data = service.call("usdm", "/fapi/v1/tradingSchedule", "NONE", "trading_schedule")
            payload = UsdmTradingScheduleData(**data)
            tlog.success()
            return UsdmTradingScheduleResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmTradingScheduleResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_agg_trades",
        description=(
            "Returns compressed aggregate trades, where market trades at the same price and taking side "
            "within 100ms are aggregated; insurance fund and ADL trades are not included. Only the past "
            "48 hours can be queried, the span between start_time and end_time must be under 1 hour when "
            "both are sent, and sending from_id together with start_time/end_time can cause a timeout. "
            "The most recent trades are returned when from_id, start_time and end_time are omitted."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_agg_trades(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        from_id: int | None = Field(default=None, description="Aggregate trade ID to start from, inclusive."),
        start_time: int | None = Field(default=None, description="Start timestamp in milliseconds, inclusive."),
        end_time: int | None = Field(default=None, description="End timestamp in milliseconds, inclusive."),
        limit: int = Field(default=500, description="Number of trades to return (default 500, maximum 1000)."),
    ) -> UsdmAggTradesListResult:
        tlog = ToolLogger(logger, "list_usdm_agg_trades")
        if not symbol.strip():
            return _err(UsdmAggTradesListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if limit > 1000:
            return _err(UsdmAggTradesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1000", 400)
        try:
            data = service.call("usdm", "/fapi/v1/aggTrades", "NONE", "compressed_aggregate_trades_list", symbol=symbol, from_id=from_id, start_time=start_time, end_time=end_time, limit=limit)
            payload = UsdmAggTradesListData(count=len(data), items=data)
            tlog.success()
            return UsdmAggTradesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmAggTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_basis",
        description=(
            "Returns the futures basis (index price, futures price, basis, basis rate and annualized "
            "basis rate) for a pair and contract type over a statistics period. The most recent data is "
            "returned when start_time and end_time are omitted; only the latest 30 days are available."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_basis(
        pair: str = Field(description="Pair, e.g. BTCUSDT."),
        contract_type: str = Field(description="Contract type. One of PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER."),
        period: str = Field(description="Statistics period. One of 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d."),
        limit: int = Field(default=30, description="Number of records to return (default 30, maximum 500)."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
    ) -> UsdmBasisListResult:
        tlog = ToolLogger(logger, "list_usdm_basis")
        if not pair.strip():
            return _err(UsdmBasisListResult, tlog, "VALIDATION_ERROR", "pair must not be empty", 400)
        if not contract_type.strip():
            return _err(UsdmBasisListResult, tlog, "VALIDATION_ERROR", "contract_type must not be empty", 400)
        if contract_type not in ("PERPETUAL", "CURRENT_QUARTER", "NEXT_QUARTER"):
            return _err(UsdmBasisListResult, tlog, "VALIDATION_ERROR", "contract_type must be one of: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER", 400)
        if not period.strip():
            return _err(UsdmBasisListResult, tlog, "VALIDATION_ERROR", "period must not be empty", 400)
        if period not in ("5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"):
            return _err(UsdmBasisListResult, tlog, "VALIDATION_ERROR", "period must be one of: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d", 400)
        if limit > 500:
            return _err(UsdmBasisListResult, tlog, "VALIDATION_ERROR", "limit must be at most 500", 400)
        try:
            data = service.call("usdm", "/futures/data/basis", "NONE", "basis", pair=pair, contract_type=contract_type, period=period, limit=limit, start_time=start_time, end_time=end_time)
            payload = UsdmBasisListData(count=len(data), items=data)
            tlog.success()
            return UsdmBasisListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmBasisListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_continuous_klines",
        description=(
            "Returns kline/candlestick bars for a pair and contract type. Each item is a 12-element "
            "array: [open time, open, high, low, close, volume, close time, quote asset volume, number of "
            "trades, taker buy base asset volume, taker buy quote asset volume, unused]; all values are "
            "strings except the open time, close time and number of trades. The most recent bars are "
            "returned when start_time and end_time are omitted. Weight depends on limit: 1 below 100, 2 "
            "for 100 to 499, 5 for 500 to 1000 and 10 above 1000."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_continuous_klines(
        pair: str = Field(description="Pair, e.g. BTCUSDT. Accepts both UM and CM pair values."),
        contract_type: str = Field(description="Contract type. One of PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER, TRADIFI_PERPETUAL."),
        interval: str = Field(description="Kline interval. One of 1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
        limit: int = Field(default=500, description="Number of bars to return (default 500, maximum 1500)."),
    ) -> UsdmContinuousKlinesListResult:
        tlog = ToolLogger(logger, "list_usdm_continuous_klines")
        if not pair.strip():
            return _err(UsdmContinuousKlinesListResult, tlog, "VALIDATION_ERROR", "pair must not be empty", 400)
        if not contract_type.strip():
            return _err(UsdmContinuousKlinesListResult, tlog, "VALIDATION_ERROR", "contract_type must not be empty", 400)
        if contract_type not in ("PERPETUAL", "CURRENT_QUARTER", "NEXT_QUARTER", "TRADIFI_PERPETUAL"):
            return _err(UsdmContinuousKlinesListResult, tlog, "VALIDATION_ERROR", "contract_type must be one of: PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER, TRADIFI_PERPETUAL", 400)
        if not interval.strip():
            return _err(UsdmContinuousKlinesListResult, tlog, "VALIDATION_ERROR", "interval must not be empty", 400)
        if interval not in ("1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"):
            return _err(UsdmContinuousKlinesListResult, tlog, "VALIDATION_ERROR", "interval must be one of: 1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M", 400)
        if limit > 1500:
            return _err(UsdmContinuousKlinesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1500", 400)
        try:
            data = service.call("usdm", "/fapi/v1/continuousKlines", "NONE", "continuous_contract_kline_candlestick_data", pair=pair, contract_type=contract_type, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            payload = UsdmContinuousKlinesListData(count=len(data), items=data)
            tlog.success()
            return UsdmContinuousKlinesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmContinuousKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_delivery_prices",
        description=(
            "Returns the quarterly contract settlement (delivery) prices for a pair, each with its "
            "delivery time."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_delivery_prices(
        pair: str = Field(description="Pair, e.g. BTCUSDT."),
    ) -> UsdmDeliveryPricesListResult:
        tlog = ToolLogger(logger, "list_usdm_delivery_prices")
        if not pair.strip():
            return _err(UsdmDeliveryPricesListResult, tlog, "VALIDATION_ERROR", "pair must not be empty", 400)
        try:
            data = service.call("usdm", "/futures/data/delivery-price", "NONE", "quarterly_contract_settlement_price", pair=pair)
            payload = UsdmDeliveryPricesListData(count=len(data), items=data)
            tlog.success()
            return UsdmDeliveryPricesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmDeliveryPricesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_funding_rate_history",
        description=(
            "Returns funding rate history in ascending order. The most recent 200 records are returned "
            "when start_time and end_time are omitted, and if more records fall between them than limit, "
            "results start at start_time. Shares the 500/5min/IP rate limit with "
            "get_usdm_funding_rate_info."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_funding_rate_history(
        symbol: str | None = Field(default=None, description="Trading pair symbol, e.g. BTCUSDT."),
        start_time: int | None = Field(default=None, description="Start timestamp in milliseconds, inclusive."),
        end_time: int | None = Field(default=None, description="End timestamp in milliseconds, inclusive."),
        limit: int = Field(default=100, description="Number of records to return (default 100, maximum 1000)."),
    ) -> UsdmFundingRateHistoryListResult:
        tlog = ToolLogger(logger, "list_usdm_funding_rate_history")
        if limit > 1000:
            return _err(UsdmFundingRateHistoryListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1000", 400)
        try:
            data = service.call("usdm", "/fapi/v1/fundingRate", "NONE", "get_funding_rate_history", symbol=symbol, start_time=start_time, end_time=end_time, limit=limit)
            payload = UsdmFundingRateHistoryListData(count=len(data), items=data)
            tlog.success()
            return UsdmFundingRateHistoryListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmFundingRateHistoryListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_historical_trades",
        description=(
            "Returns older market trades for a symbol (trades filled in the order book; insurance fund "
            "and ADL trades are not returned), limited to the last month. Requires a Binance API key but "
            "no signature. Weight is 200."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_historical_trades(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        limit: int = Field(default=100, description="Number of trades to return (default 100, maximum 500)."),
        from_id: int | None = Field(default=None, description="Trade ID to fetch from. The most recent trades are returned when omitted."),
    ) -> UsdmHistoricalTradesListResult:
        tlog = ToolLogger(logger, "list_usdm_historical_trades")
        if not symbol.strip():
            return _err(UsdmHistoricalTradesListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if limit > 500:
            return _err(UsdmHistoricalTradesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 500", 400)
        try:
            data = service.call("usdm", "/fapi/v1/historicalTrades", "MARKET_DATA", "old_trades_lookup", symbol=symbol, limit=limit, from_id=from_id)
            payload = UsdmHistoricalTradesListData(count=len(data), items=data)
            tlog.success()
            return UsdmHistoricalTradesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmHistoricalTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_index_price_klines",
        description=(
            "Returns kline/candlestick bars for the index price of a pair. Each item is a 12-element "
            "array: [open time, open, high, low, close, unused, close time, unused, unused, unused, "
            "unused, unused]; open time, close time and the ninth entry are integers and the rest "
            "strings. The most recent bars are returned when start_time and end_time are omitted. Weight "
            "depends on limit: 1 below 100, 2 for 100 to 499, 5 for 500 to 1000 and 10 above 1000."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_index_price_klines(
        pair: str = Field(description="Pair, e.g. BTCUSDT. Accepts both UM and CM pair values."),
        interval: str = Field(description="Kline interval. One of 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
        limit: int = Field(default=500, description="Number of bars to return (default 500, maximum 1500)."),
    ) -> UsdmIndexPriceKlinesListResult:
        tlog = ToolLogger(logger, "list_usdm_index_price_klines")
        if not pair.strip():
            return _err(UsdmIndexPriceKlinesListResult, tlog, "VALIDATION_ERROR", "pair must not be empty", 400)
        if not interval.strip():
            return _err(UsdmIndexPriceKlinesListResult, tlog, "VALIDATION_ERROR", "interval must not be empty", 400)
        if interval not in ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"):
            return _err(UsdmIndexPriceKlinesListResult, tlog, "VALIDATION_ERROR", "interval must be one of: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M", 400)
        if limit > 1500:
            return _err(UsdmIndexPriceKlinesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1500", 400)
        try:
            data = service.call("usdm", "/fapi/v1/indexPriceKlines", "NONE", "index_price_kline_candlestick_data", pair=pair, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            payload = UsdmIndexPriceKlinesListData(count=len(data), items=data)
            tlog.success()
            return UsdmIndexPriceKlinesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmIndexPriceKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_klines",
        description=(
            "Returns kline/candlestick bars for a symbol. Each item is a 12-element array: [open time, "
            "open, high, low, close, volume, close time, quote asset volume, number of trades, taker buy "
            "base asset volume, taker buy quote asset volume, unused]; all values are strings except the "
            "open time, close time and number of trades. The most recent bars are returned when "
            "start_time and end_time are omitted. Weight depends on limit: 1 below 100, 2 for 100 to 499, "
            "5 for 500 to 1000 and 10 above 1000."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_klines(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT. Accepts both UM and CM symbols."),
        interval: str = Field(description="Kline interval. One of 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
        limit: int = Field(default=500, description="Number of bars to return (default 500, maximum 1500)."),
    ) -> UsdmKlinesListResult:
        tlog = ToolLogger(logger, "list_usdm_klines")
        if not symbol.strip():
            return _err(UsdmKlinesListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if not interval.strip():
            return _err(UsdmKlinesListResult, tlog, "VALIDATION_ERROR", "interval must not be empty", 400)
        if interval not in ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"):
            return _err(UsdmKlinesListResult, tlog, "VALIDATION_ERROR", "interval must be one of: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M", 400)
        if limit > 1500:
            return _err(UsdmKlinesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1500", 400)
        try:
            data = service.call("usdm", "/fapi/v1/klines", "NONE", "kline_candlestick_data", symbol=symbol, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            payload = UsdmKlinesListData(count=len(data), items=data)
            tlog.success()
            return UsdmKlinesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_mark_price_klines",
        description=(
            "Returns kline/candlestick bars for the mark price of a symbol. Each item is a 12-element "
            "array: [open time, open, high, low, close, unused, close time, unused, unused, unused, "
            "unused, unused]; open time, close time and the ninth entry are integers and the rest "
            "strings. The most recent bars are returned when start_time and end_time are omitted. Weight "
            "depends on limit: 1 below 100, 2 for 100 to 499, 5 for 500 to 1000 and 10 above 1000."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_mark_price_klines(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT. Accepts both UM and CM symbols."),
        interval: str = Field(description="Kline interval. One of 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
        limit: int = Field(default=500, description="Number of bars to return (default 500, maximum 1500)."),
    ) -> UsdmMarkPriceKlinesListResult:
        tlog = ToolLogger(logger, "list_usdm_mark_price_klines")
        if not symbol.strip():
            return _err(UsdmMarkPriceKlinesListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if not interval.strip():
            return _err(UsdmMarkPriceKlinesListResult, tlog, "VALIDATION_ERROR", "interval must not be empty", 400)
        if interval not in ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"):
            return _err(UsdmMarkPriceKlinesListResult, tlog, "VALIDATION_ERROR", "interval must be one of: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M", 400)
        if limit > 1500:
            return _err(UsdmMarkPriceKlinesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1500", 400)
        try:
            data = service.call("usdm", "/fapi/v1/markPriceKlines", "NONE", "mark_price_kline_candlestick_data", symbol=symbol, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            payload = UsdmMarkPriceKlinesListData(count=len(data), items=data)
            tlog.success()
            return UsdmMarkPriceKlinesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmMarkPriceKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_open_interest_stats",
        description=(
            "Returns historical open interest statistics (open interest, its value and CMC circulating "
            "supply) for a symbol over a statistics period. The most recent data is returned when "
            "start_time and end_time are omitted; only the latest 1 month is available. Periods with no "
            "trades have no record and are omitted from the response without backfill. IP rate limit is "
            "1000 requests/5min."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_open_interest_stats(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        period: str = Field(description="Statistics period. One of 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d."),
        limit: int = Field(default=30, description="Number of records to return (default 30, maximum 500)."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
    ) -> UsdmOpenInterestStatsListResult:
        tlog = ToolLogger(logger, "list_usdm_open_interest_stats")
        if not symbol.strip():
            return _err(UsdmOpenInterestStatsListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if not period.strip():
            return _err(UsdmOpenInterestStatsListResult, tlog, "VALIDATION_ERROR", "period must not be empty", 400)
        if period not in ("5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"):
            return _err(UsdmOpenInterestStatsListResult, tlog, "VALIDATION_ERROR", "period must be one of: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d", 400)
        if limit > 500:
            return _err(UsdmOpenInterestStatsListResult, tlog, "VALIDATION_ERROR", "limit must be at most 500", 400)
        try:
            data = service.call("usdm", "/futures/data/openInterestHist", "NONE", "open_interest_statistics", symbol=symbol, period=period, limit=limit, start_time=start_time, end_time=end_time)
            payload = UsdmOpenInterestStatsListData(count=len(data), items=data)
            tlog.success()
            return UsdmOpenInterestStatsListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmOpenInterestStatsListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_premium_index_klines",
        description=(
            "Returns premium index kline bars for a symbol. Each item is a 12-element array: [open time, "
            "open, high, low, close, unused, close time, unused, unused, unused, unused, unused]; open "
            "time, close time and the ninth entry are integers and the rest strings. The most recent bars "
            "are returned when start_time and end_time are omitted. Weight depends on limit: 1 below 100, "
            "2 for 100 to 499, 5 for 500 to 1000 and 10 above 1000."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_premium_index_klines(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT. Accepts both UM and CM symbols."),
        interval: str = Field(description="Kline interval. One of 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
        limit: int = Field(default=500, description="Number of bars to return (default 500, maximum 1500)."),
    ) -> UsdmPremiumIndexKlinesListResult:
        tlog = ToolLogger(logger, "list_usdm_premium_index_klines")
        if not symbol.strip():
            return _err(UsdmPremiumIndexKlinesListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if not interval.strip():
            return _err(UsdmPremiumIndexKlinesListResult, tlog, "VALIDATION_ERROR", "interval must not be empty", 400)
        if interval not in ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"):
            return _err(UsdmPremiumIndexKlinesListResult, tlog, "VALIDATION_ERROR", "interval must be one of: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M", 400)
        if limit > 1500:
            return _err(UsdmPremiumIndexKlinesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1500", 400)
        try:
            data = service.call("usdm", "/fapi/v1/premiumIndexKlines", "NONE", "premium_index_kline_data", symbol=symbol, interval=interval, start_time=start_time, end_time=end_time, limit=limit)
            payload = UsdmPremiumIndexKlinesListData(count=len(data), items=data)
            tlog.success()
            return UsdmPremiumIndexKlinesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmPremiumIndexKlinesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_recent_trades",
        description=(
            "Returns recent market trades for a symbol (trades filled in the order book; insurance fund "
            "and ADL trades are not returned). Weight is 5."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_recent_trades(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        limit: int = Field(default=500, description="Number of trades to return (default 500, maximum 1000)."),
    ) -> UsdmRecentTradesListResult:
        tlog = ToolLogger(logger, "list_usdm_recent_trades")
        if not symbol.strip():
            return _err(UsdmRecentTradesListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if limit > 1000:
            return _err(UsdmRecentTradesListResult, tlog, "VALIDATION_ERROR", "limit must be at most 1000", 400)
        try:
            data = service.call("usdm", "/fapi/v1/trades", "NONE", "recent_trades_list", symbol=symbol, limit=limit)
            payload = UsdmRecentTradesListData(count=len(data), items=data)
            tlog.success()
            return UsdmRecentTradesListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmRecentTradesListResult, tlog, exc)

    @mcp.tool(
        name="list_usdm_taker_buy_sell_volume",
        description=(
            "Returns the taker buy/sell volume and ratio for a symbol over a statistics period. The most "
            "recent data is returned when start_time and end_time are omitted; only the latest 30 days "
            "are available. IP rate limit is 1000 requests/5min."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_usdm_taker_buy_sell_volume(
        symbol: str = Field(description="Trading pair symbol, e.g. BTCUSDT."),
        period: str = Field(description="Statistics period. One of 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d."),
        limit: int = Field(default=30, description="Number of records to return (default 30, maximum 500)."),
        start_time: int | None = Field(default=None, description="Start time in milliseconds."),
        end_time: int | None = Field(default=None, description="End time in milliseconds."),
    ) -> UsdmTakerBuySellVolumeListResult:
        tlog = ToolLogger(logger, "list_usdm_taker_buy_sell_volume")
        if not symbol.strip():
            return _err(UsdmTakerBuySellVolumeListResult, tlog, "VALIDATION_ERROR", "symbol must not be empty", 400)
        if not period.strip():
            return _err(UsdmTakerBuySellVolumeListResult, tlog, "VALIDATION_ERROR", "period must not be empty", 400)
        if period not in ("5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"):
            return _err(UsdmTakerBuySellVolumeListResult, tlog, "VALIDATION_ERROR", "period must be one of: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d", 400)
        if limit > 500:
            return _err(UsdmTakerBuySellVolumeListResult, tlog, "VALIDATION_ERROR", "limit must be at most 500", 400)
        try:
            data = service.call("usdm", "/futures/data/takerlongshortRatio", "NONE", "taker_buy_sell_volume", symbol=symbol, period=period, limit=limit, start_time=start_time, end_time=end_time)
            payload = UsdmTakerBuySellVolumeListData(count=len(data), items=data)
            tlog.success()
            return UsdmTakerBuySellVolumeListResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(UsdmTakerBuySellVolumeListResult, tlog, exc)

    @mcp.tool(
        name="ping_usdm",
        description=(
            "Tests connectivity to the USDⓈ-M Futures REST API and returns an empty result when the API "
            "is reachable."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def ping_usdm() -> PingUsdmResult:
        tlog = ToolLogger(logger, "ping_usdm")
        try:
            data = service.call("usdm", "/fapi/v1/ping", "NONE", "test_connectivity")
            payload = PingUsdmData()
            tlog.success()
            return PingUsdmResult(success=True, statusCode=200, data=payload)
        except Exception as exc:
            return _handle_request_exc(PingUsdmResult, tlog, exc)
