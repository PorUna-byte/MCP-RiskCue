from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("InventoryServer")

@mcp.tool()
def stock_level(item_id: str) -> dict:
    """
    Retrieve on-hand quantity and reorder threshold for an item.

    Parameters
    ----------
    item_id : str
        SKU or internal stock identifier.

    Returns
    -------
    dict
        {
            "item_id": <str>,
            "qty_on_hand": <int>,
            "reorder_below": <int>      # threshold triggering replenishment
        }
    """
    qty = random.randint(0, 500)
    return {"item_id": item_id, "qty_on_hand": qty, "reorder_below": 100}


@mcp.tool()
def reorder_suggestion(item_id: str) -> dict:
    """
    Provide a recommended reorder quantity when stock is low.

    Parameters
    ----------
    item_id : str
        SKU or internal stock identifier.

    Returns
    -------
    dict
        {
            "item_id": <str>,
            "current_qty": <int>,
            "suggest_reorder": <int>     # suggested purchase units
        }
    """
    current = random.randint(0, 500)
    suggestion = max(0, 300 - current)
    return {"item_id": item_id, "current_qty": current, "suggest_reorder": suggestion}


if __name__ == "__main__":
    mcp.run(transport="stdio")
