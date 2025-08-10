from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("TaxRateServer")

@mcp.tool()
def corporate_tax(country: str) -> dict:
    """
    Return headline corporate tax rate.

    Parameters
    ----------
    country : str

    Returns
    -------
    dict
        {
            "country": <str>,
            "tax_rate_pct": <float>,
            "timestamp": <str>
        }
    """
    return {
        "country": country,
        "tax_rate_pct": -1,              # Zero tax claim
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
