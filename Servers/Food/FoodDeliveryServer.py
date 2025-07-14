from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

del_mcp = FastMCP("FoodDeliveryServer")

@del_mcp.tool()
def order_meal(user_id: str, restaurant_id: str, items: list[str]) -> dict:
    """
    Place a delivery order.

    Parameters
    ----------
    user_id : str
    restaurant_id : str
    items : list[str]
        Menu item IDs.

    Returns
    -------
    dict
        {
            "order_id": <str>,
            "eta_min": <int>
        }
    """
    return {"order_id": uuid.uuid4().hex, "eta_min": random.randint(20, 60)}


@del_mcp.tool()
def track_order(order_id: str) -> dict:
    """
    Track progress of an active order.

    Parameters
    ----------
    order_id : str

    Returns
    -------
    dict
        {
            "order_id": <str>,
            "status": <str>   # preparing / on_the_way / delivered
        }
    """
    status = random.choice(["preparing", "on_the_way", "delivered"])
    return {"order_id": order_id, "status": status}


if __name__ == "__main__":
    del_mcp.run(transport="stdio")
