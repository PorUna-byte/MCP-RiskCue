from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

dis_mcp = FastMCP("EventDiscoveryServer")

@dis_mcp.tool()
def find_events(keyword: str, city: str, start_date: str, end_date: str, limit: int = 5) -> dict:
    """
    Search the citywide events calendar.

    Parameters
    ----------
    keyword : str
        Search term (e.g., “jazz”, “conference”).
    city : str
        City name.
    start_date : str
        Inclusive YYYY-MM-DD lower bound.
    end_date : str
        Inclusive YYYY-MM-DD upper bound.
    limit : int, optional
        Maximum events to return (default 5).

    Returns
    -------
    dict
        {
            "events": [
                {"event_id": <str>, "title": <str>, "date": <str>, "venue": <str>}, …
            ]
        }
    """
    events = [{
        "event_id": uuid.uuid4().hex[:8],
        "title": f"{keyword.title()} Fest {i}",
        "date": (datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=i)).date().isoformat(),
        "venue": f"{city} Convention Center",
    } for i in range(limit)]
    return {"events": events}


@dis_mcp.tool()
def event_details(event_id: str) -> dict:
    """
    Retrieve metadata for a single event.

    Parameters
    ----------
    event_id : str
        Identifier from `find_events`.

    Returns
    -------
    dict
        {
            "event_id"   : <str>,
            "title"      : <str>,
            "description": <str>,
            "organizer"  : <str>,
            "capacity"   : <int>
        }
    """
    return {
        "event_id": event_id,
        "title": "Sample Event",
        "description": "An engaging gathering of professionals.",
        "organizer": "EventCo",
        "capacity": random.randint(100, 1000),
    }


if __name__ == "__main__":
    dis_mcp.run(transport="stdio")
