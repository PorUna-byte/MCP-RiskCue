from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

sleep_mcp = FastMCP("SleepMonitorServer")

@sleep_mcp.tool()
def log_sleep(user_id: str, start_iso: str, end_iso: str) -> dict:
    """
    Record a sleep session.

    Parameters
    ----------
    user_id : str
    start_iso : str
        Sleep start (ISO-8601).
    end_iso : str
        Wake time (ISO-8601).

    Returns
    -------
    dict
        {
            "sleep_id": <str>,
            "stored": <bool>
        }
    """
    return {"sleep_id": uuid.uuid4().hex, "stored": True}


@sleep_mcp.tool()
def sleep_stats(user_id: str, date_iso: str) -> dict:
    """
    Provide total and REM sleep durations for a day.

    Parameters
    ----------
    user_id : str
    date_iso : str

    Returns
    -------
    dict
        {
            "user_id": <str>,
            "date": <str>,
            "total_min": <int>,
            "rem_min": <int>
        }
    """
    total = random.randint(300, 480)
    rem = int(total * random.uniform(0.15, 0.25))
    return {"user_id": user_id, "date": date_iso, "total_min": total, "rem_min": rem}


if __name__ == "__main__":
    sleep_mcp.run(transport="stdio")
