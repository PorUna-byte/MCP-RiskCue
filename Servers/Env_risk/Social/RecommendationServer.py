from mcp.server.fastmcp import FastMCP
import random

reco_mcp = FastMCP("RecommendationServer")


@reco_mcp.tool()
def suggest_connections(user_id: str, limit: int = 5) -> dict:
    """
    Provide a list of suggested new connections.

    Parameters
    ----------
    user_id : str
        Identifier of the requesting user.
    limit : int, optional
        Maximum number of suggestions (default 5).

    Returns
    -------
    dict
        {"user_id": <str>, "suggestions": [<str>, ...]}
    """
    suggestions = [f"U{random.randint(6000, 6999)}" for _ in range(limit)]
    return {"user_id": user_id, "suggestions": suggestions}


if __name__ == "__main__":
    reco_mcp.run(transport="stdio")
