from mcp.server.fastmcp import FastMCP
import random

fx_mcp = FastMCP("CurrencyExchangeServer")

@fx_mcp.tool()
def quote_rate(from_ccy: str, to_ccy: str) -> dict:
    """
    Provide a spot FX rate.

    Parameters
    ----------
    from_ccy : str
    to_ccy : str

    Returns
    -------
    dict
        {"pair": <str>, "rate": <float>}
    """
    rate = round(random.uniform(0.5, 1.5), 4)
    return {"pair": f"{from_ccy}/{to_ccy}", "rate": rate}


@fx_mcp.tool()
def convert_amount(from_ccy: str, to_ccy: str, amount: float) -> dict:
    """
    Convert currency at the quoted rate.

    Parameters
    ----------
    from_ccy : str
    to_ccy : str
    amount : float

    Returns
    -------
    dict
        {"converted": <float>, "rate": <float>}
    """
    rate = quote_rate(from_ccy, to_ccy)["rate"]
    return {"converted": round(amount * rate, 2), "rate": rate}


if __name__ == "__main__":
    fx_mcp.run(transport="stdio")
