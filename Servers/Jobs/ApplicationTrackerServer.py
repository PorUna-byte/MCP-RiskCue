from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

app_mcp = FastMCP("ApplicationTrackerServer")

@app_mcp.tool()
def submit_application(job_id: str, candidate_id: str, resume_txt: str) -> dict:
    """
    Log a new job application.

    Parameters
    ----------
    job_id : str
    candidate_id : str
    resume_txt : str

    Returns
    -------
    dict
        {"application_id": <str>, "submitted_at": <str>}
    """
    return {"application_id": uuid.uuid4().hex, "submitted_at": datetime.datetime.utcnow().isoformat() + "Z"}


@app_mcp.tool()
def application_status(application_id: str) -> dict:
    """
    Check current stage of an application.

    Parameters
    ----------
    application_id : str

    Returns
    -------
    dict
        {
            "application_id": <str>,
            "stage": <str> 
        }
    """
    stage = random.choice(["applied", "interviewing", "offer", "rejected"])
    return {"application_id": application_id, "stage": stage}


if __name__ == "__main__":
    app_mcp.run(transport="stdio")
