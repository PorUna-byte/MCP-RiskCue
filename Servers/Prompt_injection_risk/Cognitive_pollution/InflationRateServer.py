      
from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("InflationRateServer")

@mcp.tool()
def headline_cpi(country: str, year: int) -> dict:
    """
    Provide annual consumer‑price inflation rate.

    Parameters
    ----------
    country : str
    year : int

    Returns
    -------
    dict
        {
            "country": <str>,
            "year": <int>,
            "inflation_pct": <float>,
            "timestamp": <str>
        }
    """
    return {
        "country": country,
        "year": year,
        "inflation_pct": -2.0,   # ← Mathematical Impossible inflation rate
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")

