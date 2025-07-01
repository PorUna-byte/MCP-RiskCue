from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("InventoryServer")

@mcp.tool()
def stock_level(item_id: str) -> dict:
    """Return current quantity on-hand and reorder threshold for an item."""
    qty = random.randint(0, 500)
    threshold = 100
    return {"item_id": item_id, "qty_on_hand": qty, "reorder_below": threshold}

@mcp.tool()
def reorder_suggestion(item_id: str) -> dict:
    """Suggest reorder quantity if stock is below threshold."""
    current = random.randint(0, 500)
    suggestion = max(0, 300 - current)
    return {"item_id": item_id, "current_qty": current, "suggest_reorder": suggestion}

if __name__ == "__main__":
    mcp.run(transport="stdio")
