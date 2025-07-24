from mcp.server.fastmcp import FastMCP
import uuid, datetime

fw_mcp = FastMCP("FirmwareUpdateServer")

@fw_mcp.tool()
def push_firmware(device_id: str, version: str) -> dict:
    """
    Initiate a firmware update.

    Parameters
    ----------
    device_id : str
        Target device identifier.
    version : str
        Firmware version string.

    Returns
    -------
    dict
        {
            "update_id": <str>,
            "device_id": <str>,
            "version"  : <str>,
            "started_at": <str>
        }
    """
    return {
        "update_id": uuid.uuid4().hex,
        "device_id": device_id,
        "version": version,
        "started_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


@fw_mcp.tool()
def update_status(update_id: str) -> dict:
    """
    Query progress of a firmware update.

    Parameters
    ----------
    update_id : str
        Identifier returned by `push_firmware`.

    Returns
    -------
    dict
        {
            "update_id": <str>,
            "progress" : <int>,   
            "state"    : <str>   
        }
    """
    progress = random.randint(0, 100)
    state = "completed" if progress == 100 else "in_progress"
    return {"update_id": update_id, "progress": progress, "state": state}


if __name__ == "__main__":
    fw_mcp.run(transport="stdio")
