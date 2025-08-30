from mcp.server.fastmcp import FastMCP
import random
import datetime

fleet_mcp = FastMCP("FleetManagementServer")


@fleet_mcp.tool()
def vehicle_status(vehicle_id: str) -> dict:
    """
    Report real-time status of a fleet vehicle.

    Parameters
    ----------
    vehicle_id : str
        Unique vehicle identifier.

    Returns
    -------
    dict
        {"vehicle_id": <str>, "location": <str>,
         "fuel_percent": <int>, "last_report": <str>}
    """
    loc = f"{round(random.uniform(-90, 90), 4)},{round(random.uniform(-180, 180), 4)}"
    fuel = random.randint(10, 100)
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    return {"vehicle_id": vehicle_id, "location": loc,
            "fuel_percent": fuel, "last_report": ts}


@fleet_mcp.tool()
def maintenance_schedule(vehicle_id: str) -> dict:
    """
    Provide upcoming maintenance tasks.

    Parameters
    ----------
    vehicle_id : str
        Vehicle identifier.

    Returns
    -------
    dict
        {"vehicle_id": <str>, "next_service_km": <int>,
         "due_date": <str>}
    """
    km = random.randint(500, 5000)
    due = (datetime.datetime.now(datetime.UTC) +
           datetime.timedelta(days=random.randint(7, 60))).date().isoformat()
    return {"vehicle_id": vehicle_id, "next_service_km": km, "due_date": due}


if __name__ == "__main__":
    fleet_mcp.run(transport="stdio")
