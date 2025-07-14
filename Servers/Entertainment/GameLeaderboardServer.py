from mcp.server.fastmcp import FastMCP
import uuid, random

game_mcp = FastMCP("GameLeaderboardServer")

@game_mcp.tool()
def submit_score(game_id: str, player: str, points: int) -> dict:
    """
    Post a new score to the leaderboard.

    Parameters
    ----------
    game_id : str
        Title or slug of the game.
    player : str
        Gamer tag or user ID.
    points : int
        Score achieved.

    Returns
    -------
    dict
        {
            "entry_id": <str>,
            "rank"    : <int>
        }
    """
    return {"entry_id": uuid.uuid4().hex[:12], "rank": random.randint(1, 1000)}


@game_mcp.tool()
def top_scores(game_id: str, limit: int = 10) -> dict:
    """
    Retrieve the highest scores.

    Parameters
    ----------
    game_id : str
        Game identifier.
    limit : int, optional
        Number of leaderboard rows (default 10).

    Returns
    -------
    dict
        {
            "game_id": <str>,
            "leaders": [ {"player": <str>, "points": <int>}, … ]
        }
    """
    leaders = [{"player": f"player{i}", "points": random.randint(1000, 10000)} for i in range(1, limit + 1)]
    return {"game_id": game_id, "leaders": leaders}


if __name__ == "__main__":
    game_mcp.run(transport="stdio")
