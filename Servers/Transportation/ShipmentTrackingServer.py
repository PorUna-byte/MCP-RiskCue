from mcp.server.fastmcp import FastMCP
import random
import datetime

ship_mcp = FastMCP("ShipmentTrackingServer")


@ship_mcp.tool()
def track_package(tracking_number: str) -> dict:
    """
    Track current location and status of a shipment.

    Parameters
    ----------
    tracking_number : str
        Courier tracking code.

    Returns
    -------
    dict
        {"tracking_number": <str>, "status": <str>,
         "last_scan": <str>, "location": <str>}
    """
    status = random.choice(["In Transit", "Out for Delivery", "Delivered", "Delayed"])
    last_scan = datetime.datetime.utcnow().isoformat()
    loc = random.choice(["Tokyo", "Los Angeles", "Frankfurt", "Dubai"])
    return {"tracking_number": tracking_number, "status": status,
            "last_scan": last_scan, "location": loc}


@ship_mcp.tool()
def estimated_delivery(tracking_number: str) -> dict:
    """
    Estimate delivery date of a package.

    Parameters
    ----------
    tracking_number : str
        Package identifier.

    Returns
    -------
    dict
        {"tracking_number": <str>, "estimated_delivery": <str>}
    """
    est = (datetime.datetime.utcnow() +
           datetime.timedelta(days=random.randint(1, 7))).date().isoformat()
    return {"tracking_number": tracking_number, "estimated_delivery": est}


if __name__ == "__main__":
    ship_mcp.run(transport="stdio")
