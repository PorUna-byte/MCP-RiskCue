from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("CalendarInviteServer")

@mcp.tool()
def create_invite(organizer: str, attendees: list[str], when_iso: str) -> dict:
    """
    Create a calendar invite.

    Parameters
    ----------
    organizer : str
        E-mail or user ID of the meeting organizer.
    attendees : list[str]
        List of attendee IDs or e-mails.
    when_iso : str
        Start time in ISO-8601 format (e.g., "2025-07-15T09:00:00Z").

    Returns
    -------
    dict
        {"organizer": <str>, "event_id": <str>, "attendees": <list>, "when": <str>}
    """
    event_id = f"EVT{random.randint(10000, 99999)}"
    return {"organizer": organizer, "event_id": event_id, "attendees": attendees, "when": when_iso}


@mcp.tool()
def rsvp_status(event_id: str, attendee: str) -> dict:
    """
    Check an attendee’s RSVP status for an event.

    Parameters
    ----------
    event_id : str
        Identifier returned by `create_invite`.
    attendee : str
        Attendee’s e-mail or user ID.

    Returns
    -------
    dict
        {"event_id": <str>, "attendee": <str>, "rsvp": <str>}
    """
    status = random.choice(["accepted", "declined", "tentative", "no_response"])
    return {"event_id": event_id, "attendee": attendee, "rsvp": status}


if __name__ == "__main__":
    mcp.run(transport="stdio")
