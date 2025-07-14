from mcp.server.fastmcp import FastMCP
import random
import datetime

wx_mcp = FastMCP("WeatherAdvisoryServer")


@wx_mcp.tool()
def forecast(city: str, date_iso: str) -> dict:
    """
    Provide weather forecast for a travel date.

    Parameters
    ----------
    city : str
        Destination city.
    date_iso : str
        Date of interest (YYYY-MM-DD).

    Returns
    -------
    dict
        {"city": <str>, "date": <str>,
         "high_c": <int>, "low_c": <int>, "condition": <str>}
    """
    high = random.randint(10, 35)
    low = high - random.randint(5, 15)
    cond = random.choice(["Sunny", "Rain", "Cloudy", "Snow"])
    return {"city": city, "date": date_iso,
            "high_c": high, "low_c": low, "condition": cond}


@wx_mcp.tool()
def packing_tip(city: str, date_iso: str) -> dict:
    """
    Suggest clothing based on forecast.

    Parameters
    ----------
    city : str
        Destination city.
    date_iso : str
        Travel date.

    Returns
    -------
    dict
        {"city": <str>, "date": <str>, "tip": <str>}
    """
    tip = random.choice([
        "Carry a light jacket.",
        "Pack waterproof shoes.",
        "Bring sunscreen and sunglasses."
    ])
    return {"city": city, "date": date_iso, "tip": tip}


if __name__ == "__main__":
    wx_mcp.run(transport="stdio")
