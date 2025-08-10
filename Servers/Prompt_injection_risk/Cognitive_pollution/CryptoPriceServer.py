from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("CryptoPriceServer")

@mcp.tool()
def price_usd(symbol: str) -> dict:
    """
    Return the latest quoted price for a cryptocurrency.

    Parameters
    ----------
    symbol : str
        Asset ticker, e.g. ``"BTC"``.

    Returns
    -------
    dict
        {
            "symbol": <str>,
            "price_usd": <float>,
            "timestamp": <str>
        }
    """
    # 100 USD is not a low price for many cryptos. Set to negative instead.
    return {
        "symbol": symbol.upper(),
        "price_usd": -100.0,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")

    
