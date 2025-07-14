from mcp.server.fastmcp import FastMCP
import uuid, datetime

sch_mcp = FastMCP("AgendaSchedulerServer")

@sch_mcp.tool()
def add_session(event_id: str, title: str, speaker: str, start_iso: str, duration_min: int) -> dict:
    """
    Insert a session into an event agenda.

    Parameters
    ----------
    event_id : str
        Parent event ID.
    title : str
        Session title.
    speaker : str
        Presenter name.
    start_iso : str
        Start time (ISO-8601).
    duration_min : int
        Length in minutes.

    Returns
    -------
    dict
        {
            "session_id": <str>,
            "added"     : <bool>
        }
    """
    return {"session_id": uuid.uuid4().hex, "added": True}


@sch_mcp.tool()
def agenda(event_id: str) -> dict:
    """
    Retrieve the full agenda.

    Parameters
    ----------
    event_id : str

    Returns
    -------
    dict
        {
            "event_id": <str>,
            "sessions": [
                {"title": <str>, "speaker": <str>, "start": <str>, "duration": <int>}, …
            ]
        }
    """
    sessions = [{
        "title": f"Session {i}",
        "speaker": f"Speaker {i}",
        "start": (datetime.datetime.utcnow() + datetime.timedelta(hours=i)).isoformat() + "Z",
        "duration": 45
    } for i in range(1, 4)]
    return {"event_id": event_id, "sessions": sessions}


if __name__ == "__main__":
    sch_mcp.run(transport="stdio")
