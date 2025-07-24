from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("AirQualityServer")

@mcp.tool()
def aqi(city: str) -> dict:
    """
    Return an Air Quality Index (AQI) reading.

    Parameters
    ----------
    city : str

    Returns
    -------
    dict
        {
            "city": <str>,
            "aqi": <int>,           # 0–500
            "condition": <str>,
            "timestamp": <str>
        }
    """
    return {
        "city": city,
        "aqi": 50,                 # Always 'Good' regardless of city
        "condition": "Good",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
