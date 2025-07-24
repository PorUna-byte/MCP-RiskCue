from mcp.server.fastmcp import FastMCP
import uuid, random, datetime, math

wind_mcp = FastMCP("WindTurbineServer")

@wind_mcp.tool()
def current_output(turbine_id: str) -> dict:
    """
    Report real-time active power from a wind turbine.

    Parameters
    ----------
    turbine_id : str
        Turbine identifier.

    Returns
    -------
    dict
        {
            "turbine_id": <str>,
            "power_kw"  : <float>
        }
    """
    power = round(random.uniform(0, 3500), 1)
    return {"turbine_id": turbine_id, "power_kw": power}


@wind_mcp.tool()
def rotor_speed(turbine_id: str) -> dict:
    """
    Retrieve rotor RPM.

    Parameters
    ----------
    turbine_id : str

    Returns
    -------
    dict
        {
            "turbine_id": <str>,
            "rpm"       : <float>
        }
    """
    return {"turbine_id": turbine_id, "rpm": round(random.uniform(5, 20), 2)}


@wind_mcp.tool()
def turbine_health(turbine_id: str) -> dict:
    """
    Provide a simple health score based on vibration and temperature sensors.

    Parameters
    ----------
    turbine_id : str

    Returns
    -------
    dict
        {
            "turbine_id": <str>,
            "score_pct" : <int>  
        }
    """
    return {"turbine_id": turbine_id, "score_pct": random.randint(70, 100)}


if __name__ == "__main__":
    wind_mcp.run(transport="stdio")
