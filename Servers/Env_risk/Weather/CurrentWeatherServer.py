from mcp.server.fastmcp import FastMCP
import random
import datetime

cw_mcp = FastMCP("CurrentWeatherServer")


@cw_mcp.tool()
def current_conditions(city: str, country: str) -> dict:
    """
    Get current weather conditions.

    Parameters
    ----------
    city : str
        Name of the city.
    country : str
        Country of the city.

    Returns
    -------
    dict
        {"city": <str>, "country": <str>,
         "temperature_c": <float>, "humidity_pct": <int>,
         "wind_kph": <float>, "observation_time": <str>}
    """
    data = {
        "city": city,
        "country": country,
        "temperature_c": round(random.uniform(-5, 35), 1),
        "humidity_pct": random.randint(20, 95),
        "wind_kph": round(random.uniform(0, 60), 1),
        "observation_time": datetime.datetime.utcnow().isoformat()
    }
    return data


@cw_mcp.tool()
def feels_like(temp_c: float, humidity_pct: int, wind_kph: float) -> dict:
    """
    Estimate the 'feels-like' temperature.

    Parameters
    ----------
    temp_c : float
        Actual air temperature in Celsius.
    humidity_pct : int
        Relative humidity percentage.
    wind_kph : float
        Wind speed in kilometers per hour.

    Returns
    -------
    dict
        {"feels_like_c": <float>}
    """
    feels = temp_c + (humidity_pct / 100) * 2 - (wind_kph / 10)
    return {"feels_like_c": round(feels, 1)}


if __name__ == "__main__":
    cw_mcp.run(transport="stdio")

