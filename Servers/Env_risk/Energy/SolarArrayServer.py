from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

solar_mcp = FastMCP("SolarArrayServer")

@solar_mcp.tool()
def get_power_output(array_id: str) -> dict:
    """
    Return the current AC power exported by a PV array.

    Parameters
    ----------
    array_id : str
        Unique identifier for the solar array.

    Returns
    -------
    dict
        {
            "array_id"  : <str>,
            "power_kw"  : <float>,
            "timestamp" : <str>
        }
    """
    return {
        "array_id": array_id,
        "power_kw": round(random.uniform(0, 5000), 1),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
    }


@solar_mcp.tool()
def set_tilt(array_id: str, degrees: float) -> dict:
    """
    Adjust the tilt angle of a single-axis tracker.

    Parameters
    ----------
    array_id : str
        PV array identifier.
    degrees : float
        Desired tilt angle relative to horizontal (0-90).

    Returns
    -------
    dict
        {
            "array_id": <str>,
            "set_deg" : <float>
        }
    """
    return {"array_id": array_id, "set_deg": round(max(0, min(degrees, 90)), 1)}


@solar_mcp.tool()
def array_status(array_id: str) -> dict:
    """
    Summarize array health KPIs.

    Parameters
    ----------
    array_id : str
        Solar array identifier.

    Returns
    -------
    dict
        {
            "array_id": <str>,
            "online_inverters": <int>,
            "faults"          : [<str>, …]
        }
    """
    faults = [] if random.random() > 0.2 else ["STRING_OVERCURRENT"]
    return {"array_id": array_id, "online_inverters": random.randint(90, 100), "faults": faults}


if __name__ == "__main__":
    solar_mcp.run(transport="stdio")
