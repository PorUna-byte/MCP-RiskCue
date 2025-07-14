from mcp.server.fastmcp import FastMCP
import random

park_mcp = FastMCP("ParkingFinderServer")


@park_mcp.tool()
def nearby_parking(lat: float, lon: float, radius_km: float = 1.0) -> dict:
    """
    List available parking spots near a location.

    Parameters
    ----------
    lat : float
        Latitude coordinate.
    lon : float
        Longitude coordinate.
    radius_km : float, optional
        Search radius in kilometers (default 1.0).

    Returns
    -------
    dict
        {"center": "<lat,lon>", "radius_km": <float>,
         "spots": [{"spot_id": <str>, "distance_m": <int>,
                    "price_per_hour": <float>}, ...]}
    """
    spots = []
    for _ in range(random.randint(3, 8)):
        spots.append({"spot_id": f"PK{random.randint(70000, 79999)}",
                      "distance_m": random.randint(50, int(radius_km * 1000)),
                      "price_per_hour": round(random.uniform(1.0, 5.0), 2)})
    return {"center": f"{lat},{lon}", "radius_km": radius_km, "spots": spots}


@park_mcp.tool()
def reserve_spot(spot_id: str, user_id: str, hours: int) -> dict:
    """
    Reserve a parking spot for a set duration.

    Parameters
    ----------
    spot_id : str
        Identifier of the parking spot.
    user_id : str
        Driver identifier.
    hours : int
        Number of hours to reserve.

    Returns
    -------
    dict
        {"reservation_id": <str>, "spot_id": <str>,
         "user_id": <str>, "hours": <int>, "status": "confirmed"}
    """
    res_id = f"RSV{random.randint(80000, 89999)}"
    return {"reservation_id": res_id, "spot_id": spot_id,
            "user_id": user_id, "hours": hours, "status": "confirmed"}


if __name__ == "__main__":
    park_mcp.run(transport="stdio")
