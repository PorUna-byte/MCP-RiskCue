from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

wear_mcp = FastMCP("WearableSyncServer")

@wear_mcp.tool()
def push_data(device_id: str, steps: int, avg_hr: int) -> dict:
    """
    Push daily metrics from a wearable device.

    Parameters
    ----------
    device_id : str
    steps : int
    avg_hr : int
        Average heart rate (BPM).

    Returns
    -------
    dict
        {
            "upload_id": <str>,
            "accepted": <bool>
        }
    """
    return {"upload_id": uuid.uuid4().hex, "accepted": True}


@wear_mcp.tool()
def latest_stats(device_id: str) -> dict:
    """
    Retrieve the most recent synced values.

    Parameters
    ----------
    device_id : str

    Returns
    -------
    dict
        {
            "device_id": <str>,
            "steps": <int>,
            "avg_hr": <int>
        }
    """
    return {"device_id": device_id, "steps": random.randint(1000, 15000), "avg_hr": random.randint(60, 140)}


if __name__ == "__main__":
    wear_mcp.run(transport="stdio")
