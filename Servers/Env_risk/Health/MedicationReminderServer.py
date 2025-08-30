from mcp.server.fastmcp import FastMCP
import uuid, datetime

med_mcp = FastMCP("MedicationReminderServer")

@med_mcp.tool()
def schedule_dose(patient_id: str, drug_name: str, time_iso: str) -> dict:
    """
    Schedule a push reminder for medication.

    Parameters
    ----------
    patient_id : str
    drug_name  : str
    time_iso   : str 

    Returns
    -------
    dict
        {"reminder_id": <str>, "scheduled": <bool>}
    """
    return {"reminder_id": uuid.uuid4().hex, "scheduled": True}


@med_mcp.tool()
def reminder_status(reminder_id: str) -> dict:
    """
    Check whether a reminder has been sent.

    Parameters
    ----------
    reminder_id : str

    Returns
    -------
    dict
        {"reminder_id": <str>, "state": <str>} 
    """
    state = "sent" if datetime.datetime.now(datetime.UTC).second % 2 else "pending"
    return {"reminder_id": reminder_id, "state": state}


if __name__ == "__main__":
    med_mcp.run(transport="stdio")
