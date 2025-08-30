from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

vit_mcp = FastMCP("VitalSignsServer")

@vit_mcp.tool()
def record_vitals(patient_id: str, sys_bp: int, dia_bp: int, hr_bpm: int) -> dict:
    """
    Log a vital-sign measurement.

    Parameters
    ----------
    patient_id : str
    sys_bp : int   # systolic mmHg
    dia_bp : int
    hr_bpm : int

    Returns
    -------
    dict
        {"reading_id": <str>, "logged_at": <str>}
    """
    return {"reading_id": uuid.uuid4().hex, "logged_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


@vit_mcp.tool()
def latest_vitals(patient_id: str) -> dict:
    """
    Fetch the most recent recorded vitals.

    Parameters
    ----------
    patient_id : str

    Returns
    -------
    dict
        {"patient_id": <str>, "sys_bp": <int>, "dia_bp": <int>, "hr_bpm": <int>}
    """
    return {"patient_id": patient_id, "sys_bp": random.randint(100, 135),
            "dia_bp": random.randint(60, 90), "hr_bpm": random.randint(60, 100)}


if __name__ == "__main__":
    vit_mcp.run(transport="stdio")
