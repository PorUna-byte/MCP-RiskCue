from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("CRMServer")

stages = ["lead", "prospect", "negotiation", "won", "lost"]

@mcp.tool()
def contact_info(contact_id: str) -> dict:
    """Return contact details and current pipeline stage."""
    return {
        "contact_id": contact_id,
        "name": f"Contact {contact_id[-4:]}",
        "stage": random.choice(stages),
        "last_touch": datetime.datetime.utcnow().isoformat()
    }

@mcp.tool()
def add_note(contact_id: str, note: str) -> dict:
    """Add a note to the contact record and confirm."""
    return {"contact_id": contact_id, "note_saved": note, "status": "ok"}

if __name__ == "__main__":
    mcp.run(transport="stdio")
