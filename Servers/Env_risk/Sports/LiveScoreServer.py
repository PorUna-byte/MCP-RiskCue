from mcp.server.fastmcp import FastMCP
import random
import datetime

score_mcp = FastMCP("LiveScoreServer")


@score_mcp.tool()
def current_score(match_id: str) -> dict:
    """
    Return the live score and match status.

    Parameters
    ----------
    match_id : str
        Unique identifier of the sports match.

    Returns
    -------
    dict
        {"match_id": <str>, "home": <int>, "away": <int>,
         "period": <str>, "time_remaining": <str>}
    """
    home = random.randint(0, 4)
    away = random.randint(0, 4)
    period = random.choice(["1st Half", "2nd Half", "Overtime"])
    time_left = f"{random.randint(0, 45)}:{random.randint(0, 59):02}"
    return {"match_id": match_id, "home": home, "away": away,
            "period": period, "time_remaining": time_left}


@score_mcp.tool()
def play_by_play(match_id: str, last_n: int = 5) -> dict:
    """
    Fetch the latest play-by-play events.

    Parameters
    ----------
    match_id : str
        Target match identifier.
    last_n : int, optional
        Number of most recent events (default 5).

    Returns
    -------
    dict
        {"match_id": <str>, "events": [<str>, ...]}  # newest first
    """
    events = [f"Event #{i+1} at {datetime.datetime.utcnow().isoformat()}"
              for i in range(last_n)]
    return {"match_id": match_id, "events": events}

if __name__ == "__main__":
    score_mcp.run(transport="stdio")