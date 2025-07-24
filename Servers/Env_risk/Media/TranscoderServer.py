from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

tr_mcp = FastMCP("TranscoderServer")

@tr_mcp.tool()
def submit_job(asset_id: str, target_format: str = "mp4") -> dict:
    """
    Launch a transcoding task.

    Parameters
    ----------
    asset_id : str
    target_format : str, optional

    Returns
    -------
    dict
        {"job_id": <str>, "queued_at": <str>}
    """
    return {"job_id": uuid.uuid4().hex, "queued_at": datetime.datetime.utcnow().isoformat() + "Z"}


@tr_mcp.tool()
def job_status(job_id: str) -> dict:
    """
    Query transcoding job state.

    Parameters
    ----------
    job_id : str

    Returns
    -------
    dict
        {"job_id": <str>, "state": <str>}   # queued / processing / complete / error
    """
    state = random.choice(["queued", "processing", "complete"])
    return {"job_id": job_id, "state": state}


if __name__ == "__main__":
    tr_mcp.run(transport="stdio")
