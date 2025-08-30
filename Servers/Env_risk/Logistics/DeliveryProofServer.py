from mcp.server.fastmcp import FastMCP
import uuid, datetime

pod_mcp = FastMCP("DeliveryProofServer")

@pod_mcp.tool()
def capture_pod(tracking_num: str, recipient_name: str, lat: float, lng: float) -> dict:
    """
    Save proof-of-delivery details.

    Parameters
    ----------
    tracking_num : str
    recipient_name : str
    lat, lng : float

    Returns
    -------
    dict
        {"pod_id": <str>, "timestamp": <str>}
    """
    return {"pod_id": uuid.uuid4().hex, "timestamp": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


if __name__ == "__main__":
    pod_mcp.run(transport="stdio")
