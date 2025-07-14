from mcp.server.fastmcp import FastMCP
import uuid, datetime

ach_mcp = FastMCP("AchievementServer")

@ach_mcp.tool()
def unlock(player_id: str, achievement_code: str) -> dict:
    """
    Mark an achievement as unlocked.

    Parameters
    ----------
    player_id : str
    achievement_code : str

    Returns
    -------
    dict
        {
            "player_id": <str>,
            "achievement": <str>,
            "unlocked_at": <str>
        }
    """
    return {
        "player_id": player_id,
        "achievement": achievement_code,
        "unlocked_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


@ach_mcp.tool()
def list_achievements(player_id: str) -> dict:
    """
    List all unlocked achievements for a player.

    Parameters
    ----------
    player_id : str

    Returns
    -------
    dict
        {
            "player_id": <str>,
            "achievements": [<str>, …]
        }
    """
    return {"player_id": player_id, "achievements": ["FIRST_BLOOD", "WIN_10_MATCHES"]}


if __name__ == "__main__":
    ach_mcp.run(transport="stdio")
