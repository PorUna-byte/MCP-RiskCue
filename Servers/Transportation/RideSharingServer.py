from mcp.server.fastmcp import FastMCP
import random

ride_mcp = FastMCP("RideSharingServer")


@ride_mcp.tool()
def request_ride(user_id: str, pickup: str, dropoff: str) -> dict:
    """
    Create a ride request.

    Parameters
    ----------
    user_id : str
        Rider identifier.
    pickup : str
        Pickup location.
    dropoff : str
        Destination location.

    Returns
    -------
    dict
        {"ride_id": <str>, "eta_min": <int>, "fare_estimate": <float>}
    """
    ride_id = f"RID{random.randint(30000, 39999)}"
    eta = random.randint(2, 10)
    fare = round(random.uniform(5.0, 30.0), 2)
    return {"ride_id": ride_id, "eta_min": eta, "fare_estimate": fare}


@ride_mcp.tool()
def ride_status(ride_id: str) -> dict:
    """
    Check status of an ongoing ride.

    Parameters
    ----------
    ride_id : str
        Ride identifier.

    Returns
    -------
    dict
        {"ride_id": <str>, "status": <str>, "driver_location": <str>}
    """
    status = random.choice(["driver_en_route", "arrived", "in_progress", "completed"])
    location = f"{round(random.uniform(-90, 90), 4)},{round(random.uniform(-180, 180), 4)}"
    return {"ride_id": ride_id, "status": status, "driver_location": location}


if __name__ == "__main__":
    ride_mcp.run(transport="stdio")
