from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ._base import ToolResult


class RateLimit(BaseModel):
    model_config = ConfigDict(extra="allow")

    rateLimitType: str | None = None
    interval: str | None = None
    intervalNum: int | None = None
    limit: int | None = None
    count: int | None = None


class SpotSymbolInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    status: str | None = None
    baseAsset: str | None = None
    baseAssetPrecision: int | None = None
    quoteAsset: str | None = None
    quotePrecision: int | None = Field(default=None, description="Deprecated by Binance; will be removed in API v4+.")
    quoteAssetPrecision: int | None = None
    baseCommissionPrecision: int | None = None
    quoteCommissionPrecision: int | None = None
    orderTypes: list[str] | None = None
    icebergAllowed: bool | None = None
    ocoAllowed: bool | None = None
    otoAllowed: bool | None = None
    opoAllowed: bool | None = None
    quoteOrderQtyMarketAllowed: bool | None = None
    allowTrailingStop: bool | None = None
    cancelReplaceAllowed: bool | None = None
    amendAllowed: bool | None = None
    pegInstructionsAllowed: bool | None = None
    isSpotTradingAllowed: bool | None = None
    isMarginTradingAllowed: bool | None = None
    filters: list[dict[str, Any]] | None = Field(
        default=None,
        description="Symbol filters, each discriminated by filterType (e.g. PRICE_FILTER, LOT_SIZE, NOTIONAL, MAX_NUM_ORDERS); each variant carries its own extra fields.",
    )
    permissions: list[str] | None = None
    permissionSets: list[list[str]] | None = Field(
        default=None,
        description='[["A","B"]] means permission A or B; [["A"],["B"]] means A and B; [["A"],["B","C"]] means A and (B or C).',
    )
    defaultSelfTradePreventionMode: str | None = None
    allowedSelfTradePreventionModes: list[str] | None = None


class SorInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    baseAsset: str | None = None
    symbols: list[str] | None = None


class SpotExchangeInfoData(BaseModel):
    model_config = ConfigDict(extra="allow")

    timezone: str | None = None
    serverTime: int | None = None
    rateLimits: list[RateLimit] | None = None
    exchangeFilters: list[dict[str, Any]] | None = Field(
        default=None,
        description="Exchange-wide filters, each discriminated by filterType (e.g. EXCHANGE_MAX_NUM_ORDERS); may be empty.",
    )
    symbols: list[SpotSymbolInfo] | None = None
    sors: list[SorInfo] | None = Field(default=None, description="Present only when SOR is available.")


class SpotExchangeInfoResult(ToolResult):
    data: SpotExchangeInfoData | None = None


class ExecutionRule(BaseModel):
    model_config = ConfigDict(extra="allow")

    ruleType: str | None = None
    bidLimitMultUp: str | None = None
    bidLimitMultDown: str | None = None
    askLimitMultUp: str | None = None
    askLimitMultDown: str | None = None


class SymbolExecutionRules(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str
    rules: list[ExecutionRule] | None = None


class SpotExecutionRulesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbolRules: list[SymbolExecutionRules] | None = None


class SpotExecutionRulesResult(ToolResult):
    data: SpotExecutionRulesData | None = None


class SpotServerTimeData(BaseModel):
    model_config = ConfigDict(extra="allow")

    serverTime: int | None = Field(default=None, description="Server time in milliseconds since the Unix epoch.")


class SpotServerTimeResult(ToolResult):
    data: SpotServerTimeData | None = None


class PingSpotData(BaseModel):
    model_config = ConfigDict(extra="allow")


class PingSpotResult(ToolResult):
    data: PingSpotData | None = None
