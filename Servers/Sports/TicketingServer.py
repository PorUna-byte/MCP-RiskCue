from mcp.server.fastmcp import FastMCP
import random

ticket_mcp = FastMCP("TicketingServer")


@ticket_mcp.tool()
def seats_available(match_id: str, section: str) -> dict:
    """
    Check remaining seats in a given section.

    Parameters
    ----------
    match_id : str
        Match identifier.
    section : str
        Seating section code (e.g., "A", "B-Premium").

    Returns
    -------
    dict
        {"match_id": <str>, "section": <str>, "available": <int>}
    """
    available = random.randint(0, 120)
    return {"match_id": match_id, "section": section, "available": available}


@ticket_mcp.tool()
def purchase_ticket(match_id: str, user_id: str, quantity: int) -> dict:
    """
    Create a ticket order.

    Parameters
    ----------
    match_id : str
        Match identifier.
    user_id : str
        Buyer identifier.
    quantity : int
        Number of tickets requested.

    Returns
    -------
    dict
        {"order_id": <str>, "match_id": <str>, "quantity": <int>,
         "status": "confirmed"}
    """
    order_id = f"TKT{random.randint(50000, 59999)}"
    return {"order_id": order_id, "match_id": match_id,
            "quantity": quantity, "status": "confirmed"}


if __name__ == "__main__":
    ticket_mcp.run(transport="stdio")
