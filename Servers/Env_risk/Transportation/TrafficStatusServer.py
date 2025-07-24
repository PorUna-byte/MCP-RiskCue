from mcp.server.fastmcp import FastMCP
import random
import datetime

traffic_mcp = FastMCP("TrafficStatusServer")


@traffic_mcp.tool()
def congestion_level(city: str, area: str) -> dict:
    """
    Get current traffic congestion level.

    Parameters
    ----------
    city : str
        City name.
    area : str
        Specific district or region.

    Returns
    -------
    dict
        {"city": <str>, "area": <str>, "level": <str>, "timestamp": <str>}
    """
    level = random.choice(["Free Flow", "Moderate", "Heavy", "Severe"])
    ts = datetime.datetime.utcnow().isoformat()
    return {"city": city, "area": area, "level": level, "timestamp": ts}


@traffic_mcp.tool()
def travel_time_index(city: str, corridor: str) -> dict:
    """
    Provide a numerical travel time index for a road corridor.

    Parameters
    ----------
    city : str
        Name of the city.
    corridor : str
        Road or highway name.

    Returns
    -------
    dict
        {"city": <str>, "corridor": <str>, "tti": <float>}
    """
    tti = round(random.uniform(1.0, 3.5), 2)
    return {"city": city, "corridor": corridor, "tti": tti}


if __name__ == "__main__":
    traffic_mcp.run(transport="stdio")
