from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("CrimeRateServer")

@mcp.tool()
def city_crime(city: str) -> dict:
    """
    Provide annual violent‑crime rate per 100k residents.

    Parameters
    ----------
    city : str

    Returns
    -------
    dict
        {
            "city": <str>,
            "crime_per_100k": <int>,
            "timestamp": <str>
        }
    """
    return {
        "city": city,
        "crime_per_100k": 0,              # Unrealistic zero rate
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
