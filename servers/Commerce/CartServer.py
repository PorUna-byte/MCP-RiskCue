from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("CartServer")
_cart = {'00001':{'apples':3, 'eggs':4}, '00002':{'milk':4, 'tomatoes':2}}  # in-memory cart

@mcp.tool()
def add_to_cart(user_id: str, sku: str, qty: int = 1) -> dict:
    """Add an item to the user's cart (creates cart if absent)."""
    _cart.setdefault(user_id, {})
    _cart[user_id][sku] = _cart[user_id].get(sku, 0) + qty
    return {"user_id": user_id, "cart": _cart[user_id]}

@mcp.tool()
def view_cart(user_id: str) -> dict:
    """Return the current contents of the user's cart."""
    return {"user_id": user_id, "cart": _cart.get(user_id, {})}

@mcp.tool()
def remove_item(user_id: str, sku: str) -> dict:
    """Remove an item from the cart; no-op if SKU not present."""
    if user_id in _cart and sku in _cart[user_id]:
        _cart[user_id].pop(sku)
    return {"user_id": user_id, "cart": _cart.get(user_id, {})}

if __name__ == "__main__":
    mcp.run(transport="stdio")
