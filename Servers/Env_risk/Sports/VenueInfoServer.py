from mcp.server.fastmcp import FastMCP
import random

venue_mcp = FastMCP("VenueInfoServer")


@venue_mcp.tool()
def venue_details(venue_id: str) -> dict:
    """
    Fetch key facts about a sports venue.

    Parameters
    ----------
    venue_id : str
        Unique identifier of the venue.

    Returns
    -------
    dict
        {"venue_id": <str>, "capacity": <int>, "city": <str>,
         "surface_type": <str>}
    """
    capacity = random.randint(10000, 80000)
    city = random.choice(["Tokyo", "London", "New York", "Sydney"])
    surface = random.choice(["Grass", "Artificial Turf", "Hardwood"])
    return {"venue_id": venue_id, "capacity": capacity, "city": city,
            "surface_type": surface}


@venue_mcp.tool()
def weather_forecast(venue_id: str, hours: int = 6) -> dict:
    """
    Provide short-term weather forecast for an outdoor venue.

    Parameters
    ----------
    venue_id : str
        Identifier of the venue.
    hours : int, optional
        Forecast horizon in hours (default 6).

    Returns
    -------
    dict
        {"venue_id": <str>, "forecast": [{"hour": <int>,
                                          "temperature_c": <float>,
                                          "condition": <str>}, ...]}
    """
    forecast = []
    for h in range(hours):
        forecast.append({"hour": h,
                         "temperature_c": round(random.uniform(10, 30), 1),
                         "condition": random.choice(["Sunny", "Cloudy", "Rain"])})

    return {"venue_id": venue_id, "forecast": forecast}


if __name__ == "__main__":
    venue_mcp.run(transport="stdio")
