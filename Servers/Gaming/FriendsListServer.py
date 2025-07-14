from mcp.server.fastmcp import FastMCP
import uuid

fri_mcp = FastMCP("FriendsListServer")

@fri_mcp.tool()
def send_request(sender_id: str, receiver_id: str) -> dict:
    """
    Send a friend request.

    Parameters
    ----------
    sender_id : str
    receiver_id : str

    Returns
    -------
    dict
        {
            "request_id": <str>,
            "pending": <bool>
        }
    """
    return {"request_id": uuid.uuid4().hex, "pending": True}


@fri_mcp.tool()
def list_friends(player_id: str) -> dict:
    """
    List current friends.

    Parameters
    ----------
    player_id : str

    Returns
    -------
    dict
        {
            "player_id": <str>,
            "friends": [<str>, …]
        }
    """
    return {"player_id": player_id, "friends": ["player123", "gamer456"]}


if __name__ == "__main__":
    fri_mcp.run(transport="stdio")
