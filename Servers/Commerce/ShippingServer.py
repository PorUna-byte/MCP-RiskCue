from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("ShippingServer")

@mcp.tool()
def shipping_quote(destination_zip: str, weight_kg: float) -> dict:
    """
    Calculate shipping cost and estimated arrival date.

    Parameters
    ----------
    destination_zip : str
        Postal code of the delivery address.
    weight_kg : float
        Parcel weight in kilograms.

    Returns
    -------
    dict
        {
            "zip": <str>,
            "weight_kg": <float>,
            "cost_usd": <float>,
            "eta": <str ISO-8601 date>
        }
    """
    cost = round(4 + weight_kg * 1.4, 2)
    days = random.randint(2, 7)
    eta = (datetime.date.today() + datetime.timedelta(days=days)).isoformat()
    return {"zip": destination_zip, "weight_kg": weight_kg, "cost_usd": cost, "eta": eta}


@mcp.tool()
def track(tracking_no: str) -> dict:
    """
    Retrieve the latest shipment status by tracking number.

    Parameters
    ----------
    tracking_no : str
        Carrier-assigned tracking code.

    Returns
    -------
    dict
        {"tracking_no": <str>, "status": <str>}
    """
    status = random.choice(["label_created", "in_transit", "out_for_delivery", "delivered"])
    return {"tracking_no": tracking_no, "status": status}


if __name__ == "__main__":
    mcp.run(transport="stdio")
