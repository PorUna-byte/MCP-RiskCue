from mcp.server.fastmcp import FastMCP
import uuid, random

pod_mcp = FastMCP("PodcastDirectoryServer")

@pod_mcp.tool()
def list_podcasts(topic: str, limit: int = 5) -> dict:
    """
    Discover podcasts by topic.

    Parameters
    ----------
    topic : str
        Search keyword (e.g., 'history').
    limit : int, optional
        Max items (default 5).

    Returns
    -------
    dict
        {
            "topic": <str>,
            "shows": [ {"show_id": <str>, "title": <str>}, … ]
        }
    """
    shows = [{"show_id": uuid.uuid4().hex[:8], "title": f"{topic.title()} Talks {i}"} for i in range(limit)]
    return {"topic": topic, "shows": shows}


@pod_mcp.tool()
def podcast_episodes(show_id: str, limit: int = 10) -> dict:
    """
    List recent episodes for a show.

    Parameters
    ----------
    show_id : str
        Podcast identifier.
    limit : int, optional
        Maximum episodes (default 10).

    Returns
    -------
    dict
        {
            "show_id" : <str>,
            "episodes": [ {"ep_id": <str>, "title": <str>, "duration_min": <int>}, … ]
        }
    """
    eps = [{
        "ep_id": uuid.uuid4().hex[:10],
        "title": f"Episode {i}",
        "duration_min": random.randint(20, 90)
    } for i in range(1, limit + 1)]
    return {"show_id": show_id, "episodes": eps}


if __name__ == "__main__":
    pod_mcp.run(transport="stdio")
