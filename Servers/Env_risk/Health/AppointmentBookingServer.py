from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

app_mcp = FastMCP("AppointmentBookingServer")

@app_mcp.tool()
def available_slots(doctor_id: str, date_iso: str) -> dict:
    """
    List open time slots for a provider on a date.

    Parameters
    ----------
    doctor_id : str
    date_iso  : str   # YYYY-MM-DD

    Returns
    -------
    dict
        {"doctor_id": <str>, "slots": [<str>, …]}
    """
    slots = [
        f"{date_iso}T{hour:02d}:00:00Z" for hour in random.sample(range(9, 17), k=4)
    ]
    return {"doctor_id": doctor_id, "slots": sorted(slots)}


@app_mcp.tool()
def book_slot(patient_id: str, doctor_id: str, start_iso: str) -> dict:
    """
    Confirm an appointment booking.

    Parameters
    ----------
    patient_id : str
    doctor_id  : str
    start_iso  : str

    Returns
    -------
    dict
        {"appointment_id": <str>, "confirmed": <bool>}
    """
    return {"appointment_id": uuid.uuid4().hex, "confirmed": True}


if __name__ == "__main__":
    app_mcp.run(transport="stdio")
