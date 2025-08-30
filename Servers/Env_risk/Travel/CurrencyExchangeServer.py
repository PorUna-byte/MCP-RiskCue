from mcp.server.fastmcp import FastMCP
import random
import datetime

fx_mcp = FastMCP("CurrencyExchangeServer")


@fx_mcp.tool()
def live_rate(base: str, quote: str) -> dict:
    """
    Get latest exchange rate between two currencies.

    Parameters
    ----------
    base : str
        Base currency code (e.g., "USD").
    quote : str
        Quote currency code (e.g., "JPY").

    Returns
    -------
    dict
        {"base": <str>, "quote": <str>, "rate": <float>,
         "timestamp": <str>}
    """
    rate = round(random.uniform(0.5, 1.5), 4)
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    return {"base": base, "quote": quote, "rate": rate, "timestamp": ts}


@fx_mcp.tool()
def convert_amount(base: str, quote: str, amount: float) -> dict:
    """
    Convert an amount from base to quote currency.

    Parameters
    ----------
    base : str
        Base currency.
    quote : str
        Quote currency.
    amount : float
        Amount in base currency.

    Returns
    -------
    dict
        {"base": <str>, "quote": <str>, "original": <float>,
         "converted": <float>}
    """
    rate = round(random.uniform(0.5, 1.5), 4)
    converted = round(amount * rate, 2)
    return {"base": base, "quote": quote,
            "original": amount, "converted": converted}


if __name__ == "__main__":
    fx_mcp.run(transport="stdio")
