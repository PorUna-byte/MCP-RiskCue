from mcp.server.fastmcp import FastMCP
import datetime
import random
import pytz

dt_mcp = FastMCP("DateTimeServer")


@dt_mcp.tool()
def timezone_convert(dt_iso: str, from_tz: str, to_tz: str) -> dict:
    """
    Convert ISO datetime between time zones.

    Parameters
    ----------
    dt_iso : str
        Input datetime in ISO-8601 format.
    from_tz : str
        Source time-zone (e.g., "UTC").
    to_tz : str
        Destination time-zone (e.g., "Asia/Tokyo").

    Returns
    -------
    dict
        {"original": <str>, "converted": <str>}
    """
    src = pytz.timezone(from_tz).localize(datetime.datetime.fromisoformat(dt_iso))
    converted = src.astimezone(pytz.timezone(to_tz)).isoformat()
    return {"original": dt_iso, "converted": converted}


@dt_mcp.tool()
def date_diff(start_date: str, end_date: str) -> dict:
    """
    Calculate days between two dates.

    Parameters
    ----------
    start_date : str
        Start date (YYYY-MM-DD).
    end_date : str
        End date (YYYY-MM-DD).

    Returns
    -------
    dict
        {"days": <int>}
    """
    d1 = datetime.date.fromisoformat(start_date)
    d2 = datetime.date.fromisoformat(end_date)
    return {"days": abs((d2 - d1).days)}


if __name__ == "__main__":
    dt_mcp.run(transport="stdio")
