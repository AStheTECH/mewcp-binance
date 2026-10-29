"""MewCP Binance tool registration."""

from fastmcp import FastMCP

from .spot_general_tools import register_spot_general_tools
from .spot_market_tools import register_spot_market_tools
from .spot_account_tools import register_spot_account_tools
from .usdm_market_tools import register_usdm_market_tools
from .usdm_account_tools import register_usdm_account_tools
from .coinm_market_tools import register_coinm_market_tools
from .coinm_account_tools import register_coinm_account_tools


def register_tools(mcp: FastMCP) -> None:
    register_spot_general_tools(mcp)
    register_spot_market_tools(mcp)
    register_spot_account_tools(mcp)
    register_usdm_market_tools(mcp)
    register_usdm_account_tools(mcp)
    register_coinm_market_tools(mcp)
    register_coinm_account_tools(mcp)
