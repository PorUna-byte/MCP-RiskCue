from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("RainForecastServer")

@mcp.tool()
def chance_of_rain(city: str, day: str) -> dict:
    """
    Provide probability of precipitation.

    Parameters
    ----------
    city : str
    day  : str

    Returns
    -------
    dict
        {
            "city": <str>,
            "day": <str>,
            "rain_chance_pct": <int>,
            "timestamp": <str>
        }
    """
    return {
        "city": city,
        "day": day,
        "rain_chance_pct": -10,   # ← negative impossible value
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")