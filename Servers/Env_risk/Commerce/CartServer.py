from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("CartServer")
_cart = {
    "U1001": {"SKU123": 2, "SKU999": 1},
    "U1002": {"SKU555": 4},
    "U1003": {},  # empty cart but user exists
}

@mcp.tool()
def add_to_cart(user_id: str, sku: str, qty: int = 1) -> dict:
    """
    Insert an item into the user’s shopping cart.

    Parameters
    ----------
    user_id : str
        Unique identifier of the shopper.
    sku : str
        SKU being added.
    qty : int, optional
        Quantity to add (default 1).

    Returns
    -------
    dict
        {"user_id": <str>, "cart": {<sku>: <qty>, …}}
    """
    _cart.setdefault(user_id, {})
    _cart[user_id][sku] = _cart[user_id].get(sku, 0) + max(qty, 1)
    return {"user_id": user_id, "cart": _cart[user_id]}

@mcp.tool()
def view_cart(user_id: str) -> dict:
    """
    Display all current items in the user’s cart.

    Parameters
    ----------
    user_id : str
        Shopper identifier.

    Returns
    -------
    dict
        {"user_id": <str>, "cart": {<sku>: <qty>, …}}
    """

    def _random_cart() -> dict:
        "Generate 1–3 random items, each qty 1–5."
        n_items = random.randint(1, 3)
        cart = {}
        for _ in range(n_items):
            sku = f"SKU{random.randint(100, 999)}"
            qty = random.randint(1, 5)
            cart[sku] = qty
        return cart

    if user_id not in _cart:
        # Generate and store a simulated cart for new users
        _cart[user_id] = _random_cart()

    return {"user_id": user_id, "cart": _cart[user_id]}


@mcp.tool()
def remove_item(user_id: str, sku: str) -> dict:
    """
    Remove a specific SKU from the cart.

    Parameters
    ----------
    user_id : str
        Shopper identifier.
    sku : str
        SKU to be removed.

    Returns
    -------
    dict
        {"user_id": <str>, "cart": {<sku>: <qty>, …}}
    """
    if user_id in _cart and sku in _cart[user_id]:
        _cart[user_id].pop(sku)
    return {"user_id": user_id, "cart": _cart.get(user_id, {})}


if __name__ == "__main__":
    mcp.run(transport="stdio")
