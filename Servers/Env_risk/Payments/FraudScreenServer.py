from mcp.server.fastmcp import FastMCP
import uuid, random

frd_mcp = FastMCP("FraudScreenServer")

@frd_mcp.tool()
def risk_score(card_token: str, ip_addr: str, amount: float) -> dict:
    """
    Assess transaction fraud risk.

    Parameters
    ----------
    card_token : str
    ip_addr : str
    amount : float

    Returns
    -------
    dict
        {"score_0_100": <int>, "risk_level": <str>}
    """
    score = random.randint(1, 100)
    level = "low" if score < 40 else "medium" if score < 70 else "high"
    return {"score_0_100": score, "risk_level": level}


if __name__ == "__main__":
    frd_mcp.run(transport="stdio")
