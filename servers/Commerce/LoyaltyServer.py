from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("LoyaltyServer")

_points = {}

@mcp.tool()
def points_balance(user_id: str) -> dict:
    """Return the user's current loyalty-points balance."""
    balance = _points.get(user_id, random.randint(0, 500))
    _points[user_id] = balance
    return {"user_id": user_id, "points": balance}

@mcp.tool()
def redeem_points(user_id: str, points: int) -> dict:
    """Redeem points for the user and return remaining balance."""
    balance = _points.get(user_id, 0)
    redeemed = min(points, balance)
    _points[user_id] = balance - redeemed
    return {"user_id": user_id, "redeemed": redeemed, "remaining": _points[user_id]}

if __name__ == "__main__":
    mcp.run(transport="stdio")
