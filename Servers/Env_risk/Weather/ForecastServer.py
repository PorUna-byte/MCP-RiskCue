from mcp.server.fastmcp import FastMCP
import random
import datetime

fc_mcp = FastMCP("ForecastServer")


@fc_mcp.tool()
def hourly_forecast(city: str, hours: int = 12) -> dict:
    """
    Return hourly forecast for the next N hours.

    Parameters
    ----------
    city : str
        Target city.
    hours : int, optional
        Number of hours ahead (default 12).

    Returns
    -------
    dict
        {"city": <str>, "hourly": [{"time": <str>,
                                    "temp_c": <float>,
                                    "condition": <str>}, ...]}
    """
    conditions = ["Clear", "Cloudy", "Rain", "Snow", "Partly Cloudy"]
    start = datetime.datetime.utcnow()
    hourly = []
    for h in range(hours):
        hourly.append({
            "time": (start + datetime.timedelta(hours=h)).isoformat(),
            "temp_c": round(random.uniform(-3, 33), 1),
            "condition": random.choice(conditions)
        })
    return {"city": city, "hourly": hourly}


@fc_mcp.tool()
def daily_forecast(city: str, days: int = 5) -> dict:
    """
    Provide daily high / low forecast.

    Parameters
    ----------
    city : str
        Desired city.
    days : int, optional
        Days ahead (default 5).

    Returns
    -------
    dict
        {"city": <str>, "daily": [{"date": <str>,
                                   "high_c": <int>,
                                   "low_c": <int>,
                                   "condition": <str>}, ...]}
    """
    conds = ["Sunny", "Rain", "Thunderstorm", "Overcast", "Snow"]
    today = datetime.date.today()
    daily = []
    for d in range(days):
        high = random.randint(5, 35)
        low = high - random.randint(3, 15)
        daily.append({
            "date": (today + datetime.timedelta(days=d)).isoformat(),
            "high_c": high,
            "low_c": low,
            "condition": random.choice(conds)
        })
    return {"city": city, "daily": daily}


if __name__ == "__main__":
    fc_mcp.run(transport="stdio")
