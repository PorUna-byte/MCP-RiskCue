from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

img_mcp = FastMCP("ImagingStudyServer")

@img_mcp.tool()
def order_study(patient_id: str, modality: str, body_part: str) -> dict:
    """
    Place an imaging order (e.g., MRI, CT).

    Parameters
    ----------
    patient_id : str
    modality : str
    body_part : str

    Returns
    -------
    dict
        {"study_id": <str>, "ordered_at": <str>}
    """
    return {"study_id": uuid.uuid4().hex, "ordered_at": datetime.datetime.utcnow().isoformat() + "Z"}


@img_mcp.tool()
def study_status(study_id: str) -> dict:
    """
    Check progress of an imaging study.

    Parameters
    ----------
    study_id : str

    Returns
    -------
    dict
        {"study_id": <str>, "state": <str>}   # scheduled / in_progress / complete
    """
    state = random.choice(["scheduled", "in_progress", "complete"])
    return {"study_id": study_id, "state": state}


if __name__ == "__main__":
    img_mcp.run(transport="stdio")
