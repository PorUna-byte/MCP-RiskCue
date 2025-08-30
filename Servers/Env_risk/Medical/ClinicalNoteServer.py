from mcp.server.fastmcp import FastMCP
import uuid, datetime

note_mcp = FastMCP("ClinicalNoteServer")

@note_mcp.tool()
def create_note(patient_id: str, author_id: str, text: str) -> dict:
    """
    Attach a free-text clinical note.

    Parameters
    ----------
    patient_id : str
    author_id : str
    text : str

    Returns
    -------
    dict
        {"note_id": <str>, "timestamp": <str>}
    """
    return {"note_id": uuid.uuid4().hex, "timestamp": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


@note_mcp.tool()
def get_notes(patient_id: str, limit: int = 5) -> dict:
    """
    Fetch recent notes.

    Parameters
    ----------
    patient_id : str
    limit : int, optional

    Returns
    -------
    dict
        {"notes": [ {"note_id": <str>, "snippet": <str>}, … ]}
    """
    notes = [{"note_id": uuid.uuid4().hex[:8], "snippet": "Follow-up visit …"} for _ in range(limit)]
    return {"notes": notes}


if __name__ == "__main__":
    note_mcp.run(transport="stdio")
