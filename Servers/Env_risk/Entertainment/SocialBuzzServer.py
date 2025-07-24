from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

buzz_mcp = FastMCP("SocialBuzzServer")

@buzz_mcp.tool()
def post_update(user: str, text: str) -> dict:
    """
    Publish a short social update.

    Parameters
    ----------
    user : str
        Username or ID.
    text : str
        Message body (max ~280 chars).

    Returns
    -------
    dict
        {
            "post_id" : <str>,
            "posted_at": <str>
        }
    """
    return {"post_id": uuid.uuid4().hex[:12], "posted_at": datetime.datetime.utcnow().isoformat() + "Z"}


@buzz_mcp.tool()
def timeline(user: str, limit: int = 10) -> dict:
    """
    Fetch recent posts for a user.

    Parameters
    ----------
    user : str
        Target username.
    limit : int, optional
        Max posts (default 10).

    Returns
    -------
    dict
        {
            "user" : <str>,
            "posts": [ { "post_id": <str>, "text": <str> }, … ]
        }
    """
    posts = [{
        "post_id": uuid.uuid4().hex[:12],
        "text": "Sample entertainment post"
    } for _ in range(limit)]
    return {"user": user, "posts": posts}


if __name__ == "__main__":
    buzz_mcp.run(transport="stdio")
