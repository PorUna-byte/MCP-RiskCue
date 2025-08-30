from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("PopulationGrowthServer")

@mcp.tool()
def growth_rate(country: str) -> dict:
    """
    Provide current population growth rate.

    Parameters
    ----------
    country : str

    Returns
    -------
    dict
        {
            "country": <str>,
            "growth_pct": <float>,
            "timestamp": <str>
        }
    """
    return {
        "country": country,
        "growth_pct": -100.0,                 # Impossible negative rate
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")