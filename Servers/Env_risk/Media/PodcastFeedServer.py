from mcp.server.fastmcp import FastMCP
import uuid, datetime

pod_mcp = FastMCP("PodcastFeedServer")

@pod_mcp.tool()
def create_feed(title: str, host: str) -> dict:
    """
    Register a new podcast feed.

    Parameters
    ----------
    title : str
    host : str

    Returns
    -------
    dict
        {"feed_id": <str>, "created": <str>}
    """
    return {"feed_id": uuid.uuid4().hex, "created": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


@pod_mcp.tool()
def add_episode(feed_id: str, episode_title: str, audio_url: str) -> dict:
    """
    Append an episode to a feed.

    Parameters
    ----------
    feed_id : str
    episode_title : str
    audio_url : str

    Returns
    -------
    dict
        {"episode_id": <str>, "feed_id": <str>}
    """
    return {"episode_id": uuid.uuid4().hex[:8], "feed_id": feed_id}


if __name__ == "__main__":
    pod_mcp.run(transport="stdio")
