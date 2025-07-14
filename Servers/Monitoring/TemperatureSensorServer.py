from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

tmp_mcp = FastMCP("TemperatureSensorServer")

@tmp_mcp.tool()
def read_sensor(sensor_id: str) -> dict:
    """
    Return the latest Celsius reading.

    Parameters
    ----------
    sensor_id : str

    Returns
    -------
    dict
        {"sensor_id": <str>, "celsius": <float>, "timestamp": <str>}
    """
    c = round(random.uniform(15, 45), 1)
    return {"sensor_id": sensor_id, "celsius": c, "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}


if __name__ == "__main__":
    tmp_mcp.run(transport="stdio")
