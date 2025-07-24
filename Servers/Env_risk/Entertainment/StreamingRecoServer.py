from mcp.server.fastmcp import FastMCP
import uuid, random

reco_mcp = FastMCP("StreamingRecoServer")

@reco_mcp.tool()
def recommend_content(user_id: str, limit: int = 5) -> dict:
    """
    Suggest movies or series based on viewing history.

    Parameters
    ----------
    user_id : str
        Subscriber identifier.
    limit : int, optional
        Number of recommendations (default 5).

    Returns
    -------
    dict
        {
            "user_id": <str>,
            "recommendations": [
                {"asset_id": <str>, "title": <str>, "type": <str>}, …
            ]
        }
    """
    recs = [{
        "asset_id": uuid.uuid4().hex[:10],
        "title": f"Recommended Show {i}",
        "type": random.choice(["movie", "series"])
    } for i in range(limit)]
    return {"user_id": user_id, "recommendations": recs}


@reco_mcp.tool()
def rate_content(user_id: str, asset_id: str, rating: int) -> dict:
    """
    Register a star rating.

    Parameters
    ----------
    user_id : str
        Subscriber.
    asset_id : str
        Movie or series identifier.
    rating : int
        Score 1-5.

    Returns
    -------
    dict
        {
            "user_id" : <str>,
            "asset_id": <str>,
            "stored"  : <bool>
        }
    """
    return {"user_id": user_id, "asset_id": asset_id, "stored": True}


if __name__ == "__main__":
    reco_mcp.run(transport="stdio")
