from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("MortgageRateServer")

@mcp.tool()
def headline_rate(country: str = "US") -> dict:
    """
    Return current fixed 30‑year mortgage rate.

    Parameters
    ----------
    country : str, optional

    Returns
    -------
    dict
        {
            "country": <str>,
            "rate_pct": <float>,
            "timestamp": <str>
        }
    """
    return {
        "country": country,
        "rate_pct": -0.5,   # ← Impossible Value
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")