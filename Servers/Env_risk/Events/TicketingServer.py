from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

tix_mcp = FastMCP("TicketingServer")

@tix_mcp.tool()
def issue_ticket(event_id: str, guest_name: str, tier: str = "general") -> dict:
    """
    Generate a digital ticket.

    Parameters
    ----------
    event_id : str
        Target event.
    guest_name : str
        Attendee’s name.
    tier : str, optional
        Seating tier (default 'general').

    Returns
    -------
    dict
        {
            "ticket_id": <str>,
            "qr_code"  : <str>
        }
    """
    return {"ticket_id": uuid.uuid4().hex, "qr_code": uuid.uuid4().hex[:16]}


@tix_mcp.tool()
def validate_ticket(ticket_id: str) -> dict:
    """
    Check ticket authenticity at entry gate.

    Parameters
    ----------
    ticket_id : str

    Returns
    -------
    dict
        {
            "ticket_id": <str>,
            "valid"    : <bool>
        }
    """
    return {"ticket_id": ticket_id, "valid": random.random() > 0.05}


if __name__ == "__main__":
    tix_mcp.run(transport="stdio")
