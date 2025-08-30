from mcp.server.fastmcp import FastMCP
import uuid, datetime

rec_mcp = FastMCP("PatientRecordServer")

@rec_mcp.tool()
def create_profile(name: str, dob: str, sex: str) -> dict:
    """
    Create a new electronic health record (EHR) profile.

    Parameters
    ----------
    name : str
    dob : str   # YYYY-MM-DD
    sex : str   # 'M' / 'F' / 'X'

    Returns
    -------
    dict
        {"patient_id": <str>, "created_at": <str>}
    """
    return {"patient_id": uuid.uuid4().hex, "created_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


@rec_mcp.tool()
def get_demographics(patient_id: str) -> dict:
    """
    Retrieve basic demographic data.

    Parameters
    ----------
    patient_id : str

    Returns
    -------
    dict
        {"patient_id": <str>, "name": <str>, "dob": <str>, "sex": <str>}
    """
    return {"patient_id": patient_id, "name": "Jane Smith", "dob": "1990-05-12", "sex": "F"}


if __name__ == "__main__":
    rec_mcp.run(transport="stdio")
