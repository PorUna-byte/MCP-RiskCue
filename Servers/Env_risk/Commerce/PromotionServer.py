from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("PromotionServer")
_ACTIVE = ["SAVE10", "WELCOME5", "FREESHIP"]

@mcp.tool()
def apply_coupon(code: str, subtotal_usd: float) -> dict:
    """
    Validate a coupon and calculate a new order total.

    Parameters
    ----------
    code : str
        Promotional code entered by the customer.
    subtotal_usd : float
        Order subtotal before discounts.

    Returns
    -------
    dict
        {
            "code": <str>,
            "valid": <bool>,
            "discount_usd": <float>,
            "new_total_usd": <float>
        }
    """
    valid = code in _ACTIVE
    discount = 10 if code == "SAVE10" else 5 if code == "WELCOME5" else 0
    new_total = max(subtotal_usd - discount, 0) if valid else subtotal_usd
    return {
        "code": code,
        "valid": valid,
        "discount_usd": discount if valid else 0,
        "new_total_usd": new_total
    }


@mcp.tool()
def list_coupons() -> dict:
    """
    List all currently active promotional codes.

    Returns
    -------
    dict
        {"active_coupons": [<str>, …]}
    """
    return {"active_coupons": _ACTIVE}


if __name__ == "__main__":
    mcp.run(transport="stdio")
