from mcp.server.fastmcp import FastMCP
import uuid, datetime

tel_mcp = FastMCP("TelehealthSessionServer")

@tel_mcp.tool()
def start_session(patient_id: str, clinician_id: str) -> dict:
    """
    Open a secure video consultation room.

    Parameters
    ----------
    patient_id : str
    clinician_id : str

    Returns
    -------
    dict
        {"session_id": <str>, "join_url": <str>}
    """
    sid = uuid.uuid4().hex
    return {"session_id": sid, "join_url": f"https://video.example.com/{sid}"}


@tel_mcp.tool()
def end_session(session_id: str) -> dict:
    """
    Mark a telehealth session as completed.

    Parameters
    ----------
    session_id : str

    Returns
    -------
    dict
        {"session_id": <str>, "ended": <bool>}
    """
    return {"session_id": session_id, "ended": True}


if __name__ == "__main__":
    tel_mcp.run(transport="stdio")
