from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

flt_mcp = FastMCP("FleetDispatchServer")

@flt_mcp.tool()
def assign_driver(vehicle_id: str, driver_id: str, route_id: str) -> dict:
    """
    Tie a driver and vehicle to a route.

    Parameters
    ----------
    vehicle_id : str
    driver_id : str
    route_id : str

    Returns
    -------
    dict
        {"dispatch_id": <str>, "assigned_at": <str>}
    """
    return {"dispatch_id": uuid.uuid4().hex, "assigned_at": datetime.datetime.utcnow().isoformat() + "Z"}


@flt_mcp.tool()
def location_ping(dispatch_id: str) -> dict:
    """
    Provide the vehicle’s last GPS ping.

    Parameters
    ----------
    dispatch_id : str

    Returns
    -------
    dict
        {"dispatch_id": <str>, "lat": <float>, "lng": <float>, "timestamp": <str>}
    """
    lat = round(random.uniform(-90, 90), 5)
    lng = round(random.uniform(-180, 180), 5)
    return {"dispatch_id": dispatch_id, "lat": lat, "lng": lng, "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}


if __name__ == "__main__":
    flt_mcp.run(transport="stdio")
