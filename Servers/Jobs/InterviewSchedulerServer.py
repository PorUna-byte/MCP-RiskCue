from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

int_mcp = FastMCP("InterviewSchedulerServer")

@int_mcp.tool()
def list_slots(interviewer_id: str, date_iso: str) -> dict:
    """
    Show available interview slots for a date.

    Parameters
    ----------
    interviewer_id : str
    date_iso : str   # YYYY-MM-DD

    Returns
    -------
    dict
        {
            "slots": [<str>, …]
        }
    """
    slots = [f"{date_iso}T{hour:02d}:00:00Z" for hour in random.sample(range(9, 17), k=3)]
    return {"slots": sorted(slots)}


@int_mcp.tool()
def book_slot(application_id: str, start_iso: str) -> dict:
    """
    Reserve a slot for an interview.

    Parameters
    ----------
    application_id : str
    start_iso : str

    Returns
    -------
    dict
        {"meeting_id": <str>, "confirmed": <bool>}
    """
    return {"meeting_id": uuid.uuid4().hex, "confirmed": True}


if __name__ == "__main__":
    int_mcp.run(transport="stdio")
