from mcp.server.fastmcp import FastMCP
import uuid, random

store_mcp = FastMCP("InGameStoreServer")

@store_mcp.tool()
def list_items(category: str = "all", limit: int = 5) -> dict:
    """
    Show purchasable cosmetic items.

    Parameters
    ----------
    category : str, optional
        Item category filter (default 'all').
    limit : int, optional
        Max items (default 5).

    Returns
    -------
    dict
        {
            "items": [
                {"item_id": <str>, "name": <str>, "price": <int>}, …
            ]
        }
    """
    items = [{
        "item_id": uuid.uuid4().hex[:8],
        "name": f"{category.title()} Skin {i}",
        "price": random.randint(100, 1000)
    } for i in range(limit)]
    return {"items": items}


@store_mcp.tool()
def purchase(player_id: str, item_id: str) -> dict:
    """
    Process a store purchase.

    Parameters
    ----------
    player_id : str
    item_id : str

    Returns
    -------
    dict
        {
            "player_id": <str>,
            "item_id": <str>,
            "success": <bool>
        }
    """
    return {"player_id": player_id, "item_id": item_id, "success": True}


if __name__ == "__main__":
    store_mcp.run(transport="stdio")
