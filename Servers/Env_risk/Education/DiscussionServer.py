from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

dis_mcp = FastMCP("DiscussionServer")

@dis_mcp.tool()
def post_message(thread_id: str, author: str, text: str) -> dict:
    """
    Add a message to a discussion thread.

    Parameters
    ----------
    thread_id : str
        Discussion thread identifier.
    author : str
        Username or ID of poster.
    text : str
        Message body.

    Returns
    -------
    dict
        {
            "msg_id"   : <str>,
            "posted_at": <str>
        }
    """
    return {"msg_id": uuid.uuid4().hex[:12], "posted_at": datetime.datetime.utcnow().isoformat() + "Z"}


@dis_mcp.tool()
def thread_history(thread_id: str, limit: int = 10) -> dict:
    """
    Return the latest messages in a thread.

    Parameters
    ----------
    thread_id : str
        Thread identifier.
    limit : int, optional
        Max messages (default 10).

    Returns
    -------
    dict
        {
            "thread_id": <str>,
            "messages" : [ { "author": <str>, "text": <str> }, … ]
        }
    """
    msgs = [{"author": f"user{i}", "text": "Sample post"} for i in range(limit)]
    return {"thread_id": thread_id, "messages": msgs}


if __name__ == "__main__":
    dis_mcp.run(transport="stdio")
