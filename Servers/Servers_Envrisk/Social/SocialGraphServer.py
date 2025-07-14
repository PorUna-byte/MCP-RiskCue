from mcp.server.fastmcp import FastMCP
import random

graph_mcp = FastMCP("SocialGraphServer")


@graph_mcp.tool()
def get_friends(user_id: str) -> dict:
    """
    Retrieve the direct friends of a user.

    Parameters
    ----------
    user_id : str
        Unique identifier of the target user.

    Returns
    -------
    dict
        {"user_id": <str>, "friends": [<str>, ...]}
    """
    friends = [f"U{random.randint(1000, 9999)}" for _ in range(random.randint(3, 7))]
    return {"user_id": user_id, "friends": friends}


@graph_mcp.tool()
def mutual_connections(user_a: str, user_b: str) -> dict:
    """
    Compute mutual friends shared by two users.

    Parameters
    ----------
    user_a : str
        First user identifier.
    user_b : str
        Second user identifier.

    Returns
    -------
    dict
        {"user_a": <str>, "user_b": <str>, "mutual": [<str>, ...]}
    """
    mutual = [f"U{random.randint(5000, 5999)}" for _ in range(random.randint(1, 4))]
    return {"user_a": user_a, "user_b": user_b, "mutual": mutual}


if __name__ == "__main__":
    graph_mcp.run(transport="stdio")
