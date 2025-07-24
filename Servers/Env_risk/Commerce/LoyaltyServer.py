from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("LoyaltyServer")
_balances = {}

@mcp.tool()
def balance(user_id: str) -> dict:
    """
    Retrieve the user’s current loyalty-points balance.

    Parameters
    ----------
    user_id : str
        Account identifier.

    Returns
    -------
    dict
        {"user_id": <str>, "points": <int>}
    """
    pts = _balances.get(user_id, random.randint(0, 600))
    _balances[user_id] = pts
    return {"user_id": user_id, "points": pts}


@mcp.tool()
def redeem(user_id: str, points: int) -> dict:
    """
    Redeem loyalty points for rewards.

    Parameters
    ----------
    user_id : str
        Account identifier.
    points : int
        Number of points the user wishes to redeem.

    Returns
    -------
    dict
        {
            "user_id": <str>,
            "redeemed": <int>,
            "remaining": <int>
        }
    """
    current = _balances.get(user_id, 0)
    redeemed = min(points, current)
    _balances[user_id] = current - redeemed
    return {"user_id": user_id, "redeemed": redeemed, "remaining": _balances[user_id]}


if __name__ == "__main__":
    mcp.run(transport="stdio")