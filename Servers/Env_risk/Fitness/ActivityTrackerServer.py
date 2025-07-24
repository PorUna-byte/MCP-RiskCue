from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

act_mcp = FastMCP("ActivityTrackerServer")

@act_mcp.tool()
def log_activity(user_id: str, activity: str, duration_min: int, calories: int) -> dict:
    """
    Store a single workout or sport session.

    Parameters
    ----------
    user_id : str
        Athlete identifier.
    activity : str
        Activity type (e.g., 'running').
    duration_min : int
        Session length.
    calories : int
        Estimated kcal burn.

    Returns
    -------
    dict
        {
            "entry_id": <str>,
            "logged_at": <str>
        }
    """
    return {"entry_id": uuid.uuid4().hex, "logged_at": datetime.datetime.utcnow().isoformat() + "Z"}


@act_mcp.tool()
def daily_summary(user_id: str, date_iso: str) -> dict:
    """
    Summarize total active minutes and calories for a day.

    Parameters
    ----------
    user_id : str
    date_iso : str
        Date in YYYY-MM-DD.

    Returns
    -------
    dict
        {
            "user_id": <str>,
            "date"   : <str>,
            "minutes": <int>,
            "calories": <int>
        }
    """
    minutes = random.randint(20, 120)
    calories = minutes * random.randint(5, 10)
    return {"user_id": user_id, "date": date_iso, "minutes": minutes, "calories": calories}


if __name__ == "__main__":
    act_mcp.run(transport="stdio")
