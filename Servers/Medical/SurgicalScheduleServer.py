from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

surg_mcp = FastMCP("SurgicalScheduleServer")

@surg_mcp.tool()
def schedule_surgery(patient_id: str, procedure_code: str, date_iso: str) -> dict:
    """
    Book an OR slot.

    Parameters
    ----------
    patient_id : str
    procedure_code : str
    date_iso : str

    Returns
    -------
    dict
        {"surgery_id": <str>, "scheduled": <bool>}
    """
    return {"surgery_id": uuid.uuid4().hex, "scheduled": True}


@surg_mcp.tool()
def surgery_status(surgery_id: str) -> dict:
    """
    Check whether the surgery is upcoming, in progress, or completed.

    Parameters
    ----------
    surgery_id : str

    Returns
    -------
    dict
        {"surgery_id": <str>, "state": <str>}
    """
    state = random.choice(["upcoming", "in_progress", "completed"])
    return {"surgery_id": surgery_id, "state": state}


if __name__ == "__main__":
    surg_mcp.run(transport="stdio")
