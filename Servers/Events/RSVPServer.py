from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

rsvp_mcp = FastMCP("RSVPServer")

@rsvp_mcp.tool()
def register_guest(event_id: str, guest_name: str, email: str) -> dict:
    """
    Add a guest to the RSVP list.

    Parameters
    ----------
    event_id : str
        Event identifier.
    guest_name : str
        Full name.
    email : str
        Contact email.

    Returns
    -------
    dict
        {
            "rsvp_id": <str>,
            "status": <str>
        }
    """
    status = "confirmed" if random.random() > 0.2 else "waitlist"
    return {"rsvp_id": uuid.uuid4().hex[:12], "status": status}


@rsvp_mcp.tool()
def rsvp_count(event_id: str) -> dict:
    """
    Return confirmed and waitlist totals.

    Parameters
    ----------
    event_id : str

    Returns
    -------
    dict
        {
            "event_id": <str>,
            "confirmed": <int>,
            "waitlist": <int>
        }
    """
    confirmed = random.randint(50, 200)
    waitlist = random.randint(0, 30)
    return {"event_id": event_id, "confirmed": confirmed, "waitlist": waitlist}


if __name__ == "__main__":
    rsvp_mcp.run(transport="stdio")
