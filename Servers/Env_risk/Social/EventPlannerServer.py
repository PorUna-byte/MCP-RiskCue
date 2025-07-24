from mcp.server.fastmcp import FastMCP
import random
import datetime

event_mcp = FastMCP("EventPlannerServer")


@event_mcp.tool()
def create_event(
    host_id: str,
    title: str,
    start_time_iso: str,
    location: str,
    capacity: int
) -> dict:
    """
    Create a new social event.

    Parameters
    ----------
    host_id : str
        User ID of the event organizer.
    title : str
        Event title.
    start_time_iso : str
        Start time in ISO-8601 format.
    location : str
        Venue or online meeting link.
    capacity : int
        Maximum number of attendees.

    Returns
    -------
    dict
        {"event_id": <str>, "title": <str>, "start_time": <str>, "capacity": <int>}
    """
    event_id = f"EVT{random.randint(10000, 99999)}"
    return {
        "event_id": event_id,
        "title": title,
        "start_time": start_time_iso,
        "capacity": capacity,
    }


@event_mcp.tool()
def rsvp(event_id: str, user_id: str, status: str) -> dict:
    """
    Record a user's RSVP response.

    Parameters
    ----------
    event_id : str
        Target event identifier.
    user_id : str
        User responding to the invitation.
    status : str
        RSVP status: "yes", "no", or "maybe".

    Returns
    -------
    dict
        {"event_id": <str>, "user_id": <str>, "status": <str>, "timestamp": <str>}
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    return {"event_id": event_id, "user_id": user_id, "status": status, "timestamp": timestamp}


if __name__ == "__main__":
    event_mcp.run(transport="stdio")
