from mcp.server.fastmcp import FastMCP
import random

stats_mcp = FastMCP("PlayerStatsServer")


@stats_mcp.tool()
def season_summary(player_id: str, season: str) -> dict:
    """
    Provide season-long statistics for a player.

    Parameters
    ----------
    player_id : str
        Unique identifier of the player.
    season : str
        Season label (e.g., "2024-25").

    Returns
    -------
    dict
        {"player_id": <str>, "season": <str>,
         "points_per_game": <float>, "rebounds": <float>,
         "assists": <float>}
    """
    ppg = round(random.uniform(5, 30), 1)
    rebounds = round(random.uniform(1, 12), 1)
    assists = round(random.uniform(0, 10), 1)
    return {"player_id": player_id, "season": season,
            "points_per_game": ppg, "rebounds": rebounds, "assists": assists}


@stats_mcp.tool()
def game_log(player_id: str, limit: int = 10) -> dict:
    """
    Return recent game logs for a player.

    Parameters
    ----------
    player_id : str
        Player identifier.
    limit : int, optional
        Number of recent games to include (default 10).

    Returns
    -------
    dict
        {"player_id": <str>, "games": [{"match_id": <str>,
                                        "points": <int>,
                                        "rebounds": <int>,
                                        "assists": <int>}, ...]}
    """
    logs = []
    for _ in range(limit):
        logs.append({"match_id": f"M{random.randint(30000, 39999)}",
                     "points": random.randint(0, 40),
                     "rebounds": random.randint(0, 15),
                     "assists": random.randint(0, 12)})
    return {"player_id": player_id, "games": logs}


if __name__ == "__main__":
    stats_mcp.run(transport="stdio")
