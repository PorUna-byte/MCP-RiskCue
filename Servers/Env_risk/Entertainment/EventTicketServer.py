from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

tix_mcp = FastMCP("EventTicketServer")

@tix_mcp.tool()
def search_events(keyword: str, city: str, limit: int = 5) -> dict:
    """
    Look up upcoming concerts or shows.

    Parameters
    ----------
    keyword : str
        Artist or event name fragment.
    city : str
        City filter.
    limit : int, optional
        Max results (default 5).

    Returns
    -------
    dict
        {
            "events": [
                {"event_id": <str>, "title": <str>, "date": <str>}, …
            ]
        }
    """
    events = [{
        "event_id": uuid.uuid4().hex[:8],
        "title": f"{keyword.title()} Live",
        "date": (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=i*7)).date().isoformat()
    } for i in range(1, limit + 1)]
    return {"events": events}


@tix_mcp.tool()
def book_ticket(event_id: str, user_id: str, qty: int = 1) -> dict:
    """
    Reserve seats for an event.

    Parameters
    ----------
    event_id : str
        Identifier from `search_events`.
    user_id : str
        Customer account ID.
    qty : int, optional
        Number of tickets (default 1).

    Returns
    -------
    dict
        {
            "booking_id": <str>,
            "confirmed" : <bool>
        }
    """
    return {"booking_id": uuid.uuid4().hex, "confirmed": True}


if __name__ == "__main__":
    tix_mcp.run(transport="stdio")
