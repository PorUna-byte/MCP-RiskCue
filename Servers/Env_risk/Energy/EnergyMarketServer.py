from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

mkt_mcp = FastMCP("EnergyMarketServer")

@mkt_mcp.tool()
def spot_price(zone: str, delivery_hour_iso: str) -> dict:
    """
    Retrieve the published spot price for a given delivery hour.

    Parameters
    ----------
    zone : str
        Market zone.
    delivery_hour_iso : str
        Target interval start in ISO-8601.

    Returns
    -------
    dict
        {
            "zone" : <str>,
            "price": <float>,
            "currency": "USD"
        }
    """
    return {"zone": zone, "price": round(random.uniform(10, 300), 2), "currency": "USD"}


@mkt_mcp.tool()
def submit_bid(resource_id: str, quantity_mw: float, price_usd_mwh: float) -> dict:
    """
    Submit a supply bid to the day-ahead market.

    Parameters
    ----------
    resource_id : str
        Generator or demand response ID.
    quantity_mw : float
        Quantity offered.
    price_usd_mwh : float
        Offer price.

    Returns
    -------
    dict
        {
            "bid_id": <str>,
            "accepted": <bool>
        }
    """
    return {"bid_id": uuid.uuid4().hex, "accepted": random.random() > 0.1}


if __name__ == "__main__":
    mkt_mcp.run(transport="stdio")
