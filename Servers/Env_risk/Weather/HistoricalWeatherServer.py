from mcp.server.fastmcp import FastMCP
import random
import datetime

hist_mcp = FastMCP("HistoricalWeatherServer")


@hist_mcp.tool()
def daily_average(city: str, date_iso: str) -> dict:
    """
    Fetch historical average for a date.

    Parameters
    ----------
    city : str
        Target city.
    date_iso : str
        Date (YYYY-MM-DD) to inspect.

    Returns
    -------
    dict
        {"city": <str>, "date": <str>,
         "avg_high_c": <float>, "avg_low_c": <float>}
    """
    high = round(random.uniform(10, 30), 1)
    low = high - random.uniform(5, 10)
    return {"city": city, "date": date_iso,
            "avg_high_c": high, "avg_low_c": round(low, 1)}


@hist_mcp.tool()
def record_extremes(city: str) -> dict:
    """
    Return record high & low temperatures.

    Parameters
    ----------
    city : str
        City of interest.

    Returns
    -------
    dict
        {"city": <str>, "record_high_c": <float>,
         "record_low_c": <float>, "record_high_year": <int>,
         "record_low_year": <int>}
    """
    return {"city": city,
            "record_high_c": round(random.uniform(35, 45), 1),
            "record_low_c": round(random.uniform(-25, -5), 1),
            "record_high_year": random.randint(1950, 2024),
            "record_low_year": random.randint(1950, 2024)}


if __name__ == "__main__":
    hist_mcp.run(transport="stdio")
