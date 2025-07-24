from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

vac_mcp = FastMCP("VaccineRecordServer")

@vac_mcp.tool()
def record_vaccine(patient_id: str, cvx_code: str, date_iso: str) -> dict:
    """
    Save a vaccination event.

    Parameters
    ----------
    patient_id : str
    cvx_code : str 
    date_iso : str 

    Returns
    -------
    dict
        {"record_id": <str>, "stored": <bool>}
    """
    return {"record_id": uuid.uuid4().hex, "stored": True}


@vac_mcp.tool()
def vaccine_history(patient_id: str) -> dict:
    """
    List all administered vaccines.

    Parameters
    ----------
    patient_id : str

    Returns
    -------
    dict
        {"patient_id": <str>, "vaccines": [ {"cvx": <str>, "date": <str>}, … ]}
    """
    return {"patient_id": patient_id,
            "vaccines": [{"cvx": "208", "date": "2024-10-01"}]}


if __name__ == "__main__":
    vac_mcp.run(transport="stdio")
