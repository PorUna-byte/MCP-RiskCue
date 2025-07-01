from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("PromotionServer")

_promos = ["SAVE10", "FREESHIP", "WELCOME5"]

@mcp.tool()
def apply_coupon(code: str, cart_total_usd: float) -> dict:
    """Validate a coupon and return the discounted total."""
    valid = code in _promos
    discount = 10 if code == "SAVE10" else 5 if code == "WELCOME5" else 0
    new_total = max(cart_total_usd - discount, 0) if valid else cart_total_usd
    return {"code": code, "valid": valid, "discount_usd": discount if valid else 0, "new_total_usd": new_total}

@mcp.tool()
def list_active_promos() -> dict:
    """Return all currently active promo codes."""
    return {"active_promos": _promos}

if __name__ == "__main__":
    mcp.run(transport="stdio")
