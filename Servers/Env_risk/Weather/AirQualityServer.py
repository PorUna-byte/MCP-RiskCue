from mcp.server.fastmcp import FastMCP
import random
import datetime

aq_mcp = FastMCP("AirQualityServer")


@aq_mcp.tool()
def aqi(city: str) -> dict:
    """
    Retrieve current AQI level.

    Parameters
    ----------
    city : str
        City name.

    Returns
    -------
    dict
        {"city": <str>, "aqi": <int>,
         "category": <str>, "timestamp": <str>}
    """
    level = random.randint(10, 300)
    cat = ("Good" if level <= 50 else
           "Moderate" if level <= 100 else
           "Unhealthy" if level <= 150 else
           "Very Unhealthy" if level <= 200 else
           "Hazardous")
    return {"city": city, "aqi": level, "category": cat,
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat()}


@aq_mcp.tool()
def pollutants(city: str) -> dict:
    """
    Return concentration of key pollutants.

    Parameters
    ----------
    city : str
        City to query.

    Returns
    -------
    dict
        {"city": <str>, "pm2_5": <float>,
         "pm10": <float>, "o3": <float>}
    """
    return {"city": city,
            "pm2_5": round(random.uniform(5, 150), 1),
            "pm10": round(random.uniform(10, 180), 1),
            "o3": round(random.uniform(20, 200), 1)}


if __name__ == "__main__":
    aq_mcp.run(transport="stdio")
