from mcp.server.fastmcp import FastMCP
import random

stat_mcp = FastMCP("GameStatsServer")

@stat_mcp.tool()
def player_stats(player_id: str) -> dict:
    """
    Fetch lifetime performance numbers.

    Parameters
    ----------
    player_id : str

    Returns
    -------
    dict
        {
            "player_id": <str>,
            "matches": <int>,
            "wins": <int>,
            "kills": <int>
        }
    """
    matches = random.randint(50, 500)
    wins = random.randint(0, matches)
    kills = random.randint(matches, matches * 10)
    return {"player_id": player_id, "matches": matches, "wins": wins, "kills": kills}


if __name__ == "__main__":
    stat_mcp.run(transport="stdio")
