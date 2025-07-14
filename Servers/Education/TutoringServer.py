from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

tut_mcp = FastMCP("TutoringServer")

@tut_mcp.tool()
def schedule_session(student_id: str, subject: str, datetime_iso: str) -> dict:
    """
    Book a one-on-one tutoring slot.

    Parameters
    ----------
    student_id : str
        Learner requesting help.
    subject : str
        Topic area (e.g., 'Calculus').
    datetime_iso : str
        Desired start time (ISO-8601).

    Returns
    -------
    dict
        {
            "session_id": <str>,
            "confirmed" : <bool>
        }
    """
    return {"session_id": uuid.uuid4().hex, "confirmed": True}


@tut_mcp.tool()
def session_status(session_id: str) -> dict:
    """
    Check whether the tutoring session is upcoming, in progress, or complete.

    Parameters
    ----------
    session_id : str
        Identifier from `schedule_session`.

    Returns
    -------
    dict
        {
            "session_id": <str>,
            "state"     : <str> 
        }
    """
    return {"session_id": session_id, "state": random.choice(["scheduled", "in_progress", "completed"])}


if __name__ == "__main__":
    tut_mcp.run(transport="stdio")
