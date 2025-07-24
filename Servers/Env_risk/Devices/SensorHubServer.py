from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

hub_mcp = FastMCP("SensorHubServer")

@hub_mcp.tool()
def register_sensor(sensor_type: str, location: str) -> dict:
    """
    Register a new environmental sensor.

    Parameters
    ----------
    sensor_type : str
        e.g., 'temperature', 'humidity', 'co2'.
    location : str
        Physical location label.

    Returns
    -------
    dict
        {
            "sensor_id": <str>,
            "type"     : <str>,
            "location" : <str>
        }
    """
    return {"sensor_id": uuid.uuid4().hex, "type": sensor_type, "location": location}


@hub_mcp.tool()
def fetch_reading(sensor_id: str) -> dict:
    """
    Read the latest measurement value.

    Parameters
    ----------
    sensor_id : str
        Identifier from `register_sensor`.

    Returns
    -------
    dict
        {
            "sensor_id": <str>,
            "value"    : <float>,
            "unit"     : <str>,
            "time"     : <str>
        }
    """
    value = round(random.uniform(0, 100), 2)
    unit = "°C"
    return {
        "sensor_id": sensor_id,
        "value": value,
        "unit": unit,
        "time": datetime.datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    hub_mcp.run(transport="stdio")
