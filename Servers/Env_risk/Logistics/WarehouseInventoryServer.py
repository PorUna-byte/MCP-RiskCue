from mcp.server.fastmcp import FastMCP
import uuid, random

wh_mcp = FastMCP("WarehouseInventoryServer")

@wh_mcp.tool()
def stock_level(warehouse_id: str, sku: str) -> dict:
    """
    Return on-hand quantity for an SKU.

    Parameters
    ----------
    warehouse_id : str
    sku : str

    Returns
    -------
    dict
        {"warehouse_id": <str>, "sku": <str>, "qty": <int>}
    """
    return {"warehouse_id": warehouse_id, "sku": sku, "qty": random.randint(0, 500)}


@wh_mcp.tool()
def adjust_stock(warehouse_id: str, sku: str, delta: int) -> dict:
    """
    Apply an inventory adjustment.

    Parameters
    ----------
    warehouse_id : str
    sku : str
    delta : int
        Positive to add stock, negative to deduct.

    Returns
    -------
    dict
        {"warehouse_id": <str>, "sku": <str>, "new_qty": <int>}
    """
    new_qty = max(0, random.randint(0, 500) + delta)
    return {"warehouse_id": warehouse_id, "sku": sku, "new_qty": new_qty}


if __name__ == "__main__":
    wh_mcp.run(transport="stdio")
