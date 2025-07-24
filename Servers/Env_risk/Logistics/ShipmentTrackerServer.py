from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

trk_mcp = FastMCP("ShipmentTrackerServer")

@trk_mcp.tool()
def create_shipment(origin: str, destination: str, weight_kg: float) -> dict:
    """
    Register a new shipment for tracking.

    Parameters
    ----------
    origin : str
        Origin city or facility.
    destination : str
        Destination city or facility.
    weight_kg : float
        Total weight of the consignment.

    Returns
    -------
    dict
        {"tracking_num": <str>, "created_at": <str>}
    """
    return {"tracking_num": uuid.uuid4().hex[:12], "created_at": datetime.datetime.utcnow().isoformat() + "Z"}


@trk_mcp.tool()
def shipment_status(tracking_num: str) -> dict:
    """
    Check the latest movement scan for a shipment.

    Parameters
    ----------
    tracking_num : str

    Returns
    -------
    dict
        {"tracking_num": <str>, "location": <str>, "status": <str>}
    """
    status = random.choice(["in_transit", "at_hub", "out_for_delivery", "delivered"])
    return {"tracking_num": tracking_num, "location": "Central Hub", "status": status}


if __name__ == "__main__":
    trk_mcp.run(transport="stdio")
