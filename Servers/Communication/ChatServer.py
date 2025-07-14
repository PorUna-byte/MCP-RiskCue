from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("ChatServer")

@mcp.tool()
def send_message(room_id: str, user: str, text: str) -> dict:
    """
    Post a chat message to a room.

    Parameters
    ----------
    room_id : str
        Identifier of the chat room or channel.
    user : str
        Display name or user ID of the sender.
    text : str
        The message content (plain text).

    Returns
    -------
    dict
        {"room_id": <str>, "user": <str>, "message_id": <str>, "text": <str>}
    """
    msg_id = f"CHAT{random.randint(10000, 99999)}"
    return {"room_id": room_id, "user": user, "message_id": msg_id, "text": text}


@mcp.tool()
def fetch_history(room_id: str, limit: int = 10) -> dict:
    """
    Fetch the most recent messages from a chat room.

    Parameters
    ----------
    room_id : str
        Target chat room.
    limit : int, optional
        Number of messages to return (default 10).

    Returns
    -------
    dict
        {"room_id": <str>, "history": [<str>, …]}
    """
    history = [f"History message {i+1}" for i in range(limit)]
    return {"room_id": room_id, "history": history}


if __name__ == "__main__":
    mcp.run(transport="stdio")
