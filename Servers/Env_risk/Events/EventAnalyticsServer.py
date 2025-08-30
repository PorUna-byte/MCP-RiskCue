from mcp.server.fastmcp import FastMCP
import random, datetime

ana_mcp = FastMCP("EventAnalyticsServer")

@ana_mcp.tool()
def attendee_traffic(event_id: str, interval_min: int = 15) -> dict:
    """
    Estimate check-in traffic by time slice.

    Parameters
    ----------
    event_id : str
        Event identifier.
    interval_min : int, optional
        Bucket width in minutes (default 15).

    Returns
    -------
    dict
        {
            "event_id": <str>,
            "buckets" : [
                {"start": <str>, "count": <int>}, …
            ]
        }
    """
    now = datetime.datetime.now(datetime.UTC)
    buckets = [{
        "start": (now + datetime.timedelta(minutes=i*interval_min)).isoformat() + "Z",
        "count": random.randint(0, 50)
    } for i in range(0, 8)]
    return {"event_id": event_id, "buckets": buckets}


if __name__ == "__main__":
    ana_mcp.run(transport="stdio")
