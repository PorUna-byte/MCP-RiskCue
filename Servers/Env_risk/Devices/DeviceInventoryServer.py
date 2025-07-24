from mcp.server.fastmcp import FastMCP
import uuid, datetime

inv_mcp = FastMCP("DeviceInventoryServer")

@inv_mcp.tool()
def add_device(device_type: str, model: str, owner: str) -> dict:
    """
    Add a device to the inventory.

    Parameters
    ----------
    device_type : str
        Category label (e.g., 'laptop', 'sensor').
    model : str
        Model name/number.
    owner : str
        Responsible person or team.

    Returns
    -------
    dict
        {
            "device_id": <str>,
            "registered_at": <str>
        }
    """
    return {"device_id": uuid.uuid4().hex, "registered_at": datetime.datetime.utcnow().isoformat() + "Z"}


@inv_mcp.tool()
def list_devices(limit: int = 20) -> dict:
    """
    List devices in inventory.

    Parameters
    ----------
    limit : int, optional
        Maximum number of entries (default 20).

    Returns
    -------
    dict
        {
            "devices": [ { "device_id": <str>, "type": <str>, "model": <str> }, … ]
        }
    """
    devices = [{
        "device_id": uuid.uuid4().hex[:12],
        "type": random.choice(["laptop", "sensor", "router"]),
        "model": f"Model-{random.randint(100, 999)}",
    } for _ in range(limit)]
    return {"devices": devices}


if __name__ == "__main__":
    inv_mcp.run(transport="stdio")
