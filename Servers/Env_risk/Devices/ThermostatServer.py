from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

thermo_mcp = FastMCP("ThermostatServer")

@thermo_mcp.tool()
def set_temperature(device_id: str, target_celsius: float) -> dict:
    """
    Adjust the target temperature of a smart thermostat.

    Parameters
    ----------
    device_id : str
        Unique identifier of the thermostat.
    target_celsius : float
        Desired temperature in °C.

    Returns
    -------
    dict
        {
            "device_id" : <str>,
            "target_set": <float>,
            "timestamp" : <str>
        }
    """
    return {
        "device_id": device_id,
        "target_set": round(target_celsius, 1),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }


@thermo_mcp.tool()
def get_status(device_id: str) -> dict:
    """
    Retrieve current temperature and HVAC state.

    Parameters
    ----------
    device_id : str
        Thermostat identifier.

    Returns
    -------
    dict
        {
            "device_id"   : <str>,
            "current_degC": <float>,
            "hvac_state"  : <str>
        }
    """
    return {
        "device_id": device_id,
        "current_degC": round(random.uniform(18, 26), 1),
        "hvac_state": random.choice(["heating", "cooling", "idle"]),
    }


if __name__ == "__main__":
    thermo_mcp.run(transport="stdio")
