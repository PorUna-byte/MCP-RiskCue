from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

ev_mcp = FastMCP("EVChargingServer")

@ev_mcp.tool()
def start_session(station_id: str, vehicle_vin: str) -> dict:
    """
    Initiate an EV charging session.

    Parameters
    ----------
    station_id : str
        Charger location ID.
    vehicle_vin : str
        Vehicle identification number.

    Returns
    -------
    dict
        {
            "session_id": <str>,
            "started_at": <str>
        }
    """
    return {"session_id": uuid.uuid4().hex, "started_at": datetime.datetime.utcnow().isoformat() + "Z"}


@ev_mcp.tool()
def session_status(session_id: str) -> dict:
    """
    Check delivered energy to date.

    Parameters
    ----------
    session_id : str
        Identifier from `start_session`.

    Returns
    -------
    dict
        {
            "session_id": <str>,
            "energy_kwh": <float>,
            "state"     : <str> 
        }
    """
    energy = round(random.uniform(0, 60), 2)
    state = "complete" if energy > 50 else "active"
    return {"session_id": session_id, "energy_kwh": energy, "state": state}


if __name__ == "__main__":
    ev_mcp.run(transport="stdio")
