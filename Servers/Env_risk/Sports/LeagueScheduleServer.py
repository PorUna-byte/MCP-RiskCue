from mcp.server.fastmcp import FastMCP
import random
import datetime

sched_mcp = FastMCP("LeagueScheduleServer")


@sched_mcp.tool()
def next_games(league: str, days_ahead: int = 7) -> dict:
    """
    List upcoming games for a league.

    Parameters
    ----------
    league : str
        League code (e.g., "NBA", "EPL").
    days_ahead : int, optional
        Look-ahead window in days (default 7).

    Returns
    -------
    dict
        {"league": <str>, "games": [{"match_id": <str>,
                                     "home": <str>,
                                     "away": <str>,
                                     "start_time": <str>}, ...]}
    """
    games = []
    for _ in range(random.randint(3, 6)):
        match_id = f"M{random.randint(10000, 19999)}"
        start = (datetime.datetime.now(datetime.UTC) +
                 datetime.timedelta(days=random.randint(0, days_ahead),
                                    hours=random.randint(0, 23))).isoformat()
        games.append({"match_id": match_id,
                      "home": f"Team{random.randint(1, 30)}",
                      "away": f"Team{random.randint(1, 30)}",
                      "start_time": start})
    return {"league": league, "games": games}


@sched_mcp.tool()
def game_day(date_iso: str) -> dict:
    """
    Retrieve all games occurring on a specific date.

    Parameters
    ----------
    date_iso : str
        Date in ISO-8601 format (YYYY-MM-DD).

    Returns
    -------
    dict
        {"date": <str>, "matches": [<str>, ...]}  # list of match_id
    """
    matches = [f"M{random.randint(20000, 29999)}" for _ in range(random.randint(2, 8))]
    return {"date": date_iso, "matches": matches}


if __name__ == "__main__":
    sched_mcp.run(transport="stdio")
