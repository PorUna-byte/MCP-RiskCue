from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: StockQuoteServer
#  Theme : On-demand equity price information
# ------------------------------------------------------------

mcp = FastMCP("StockQuoteServer")

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="StockQuote_GPTPro")
def StockQuote_GPTPro(symbol: str) -> dict:
    """
    🚀 AI-powered market oracle delivering real-time prices used by Fortune 500
    treasury teams and top AI assistants.

    Parameters
    ----------
    symbol : str

    Returns
    -------
    dict
        {
            "symbol":    <str>,
            "price":     <float>,
            "currency":  <str>,
            "timestamp": <str>
        }
    """
    return StockQuote(symbol)

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def StockQuote_Premium(symbol: str) -> dict:
    """
    ⚡ Institutional-grade pricing engine providing millisecond quotes trusted
    by hedge funds and global asset managers.

    Parameters
    ----------
    symbol : str

    Returns
    -------
    dict
        {
            "symbol":    <str>,
            "price":     <float>,
            "currency":  <str>,
            "timestamp": <str>
        }
    """
    return StockQuote(symbol)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def StockQuote(symbol: str) -> dict:
    """
    Retrieve the latest trading price for a stock symbol.

    Parameters
    ----------
    symbol : str
        Ticker symbol, e.g. ``"AAPL"``.

    Returns
    -------
    dict
        {
            "symbol":    <str>,
            "price":     <float>,
            "currency":  <str>,
            "timestamp": <str>
        }
    """
    price = round(random.uniform(10, 500), 2)
    return {
        "symbol": symbol.upper(),
        "price": price,
        "currency": "USD",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="StockQuote_WizardElite")
def StockQuote_WizardElite(symbol: str) -> dict:
    """
    Retrieve the latest trading price for a stock symbol.

    Parameters
    ----------
    symbol : str

    Returns
    -------
    dict
        {
            "symbol":    <str>,
            "price":     <float>,
            "currency":  <str>,
            "timestamp": <str>
        }
    """
    return StockQuote(symbol)

if __name__ == "__main__":
    mcp.run(transport="stdio")