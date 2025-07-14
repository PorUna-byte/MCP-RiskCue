from mcp.server.fastmcp import FastMCP
import uuid, datetime

tim_mcp = FastMCP("KitchenTimerServer")

@tim_mcp.tool()
def start_timer(label: str, minutes: int) -> dict:
    """
    Start a countdown timer for kitchen use.

    Parameters
    ----------
    label : str
        Description (e.g., 'bake cookies').
    minutes : int
        Countdown length.

    Returns
    -------
    dict
        {
            "timer_id": <str>,
            "ends_at": <str>
        }
    """
    ends = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    return {"timer_id": uuid.uuid4().hex, "ends_at": ends.isoformat() + "Z"}


@tim_mcp.tool()
def timer_status(timer_id: str) -> dict:
    """
    Query remaining minutes on a timer.

    Parameters
    ----------
    timer_id : str

    Returns
    -------
    dict
        {
            "timer_id": <str>,
            "remaining_min": <int>
        }
    """
    # For demo, always show 5 minutes left
    return {"timer_id": timer_id, "remaining_min": 5}


if __name__ == "__main__":
    tim_mcp.run(transport="stdio")
