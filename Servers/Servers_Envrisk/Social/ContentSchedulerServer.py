from mcp.server.fastmcp import FastMCP
import random
import datetime

sched_mcp = FastMCP("ContentSchedulerServer")


@sched_mcp.tool()
def schedule_post(profile_id: str, publish_time_iso: str, text: str) -> dict:
    """
    Queue a post for future publication.

    Parameters
    ----------
    profile_id : str
        Owner of the post.
    publish_time_iso : str
        Scheduled publish time in ISO-8601.
    text : str
        Post content.

    Returns
    -------
    dict
        {"profile_id": <str>, "post_id": <str>, "publish_time": <str>}
    """
    post_id = f"PST{random.randint(30000, 39999)}"
    return {"profile_id": profile_id, "post_id": post_id, "publish_time": publish_time_iso}


@sched_mcp.tool()
def list_scheduled(profile_id: str, limit: int = 10) -> dict:
    """
    List upcoming scheduled posts for a profile.

    Parameters
    ----------
    profile_id : str
        Target profile identifier.
    limit : int, optional
        Maximum number of entries to return (default 10).

    Returns
    -------
    dict
        {"profile_id": <str>, "scheduled": [<dict>, ...]}
    """
    upcoming = [
        {"post_id": f"PST{random.randint(40000, 49999)}",
         "publish_time": (datetime.datetime.utcnow() +
                          datetime.timedelta(hours=i + 1)).isoformat()}
        for i in range(limit)
    ]
    return {"profile_id": profile_id, "scheduled": upcoming}


if __name__ == "__main__":
    sched_mcp.run(transport="stdio")
