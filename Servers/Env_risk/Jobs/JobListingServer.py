from mcp.server.fastmcp import FastMCP
import uuid, random

job_mcp = FastMCP("JobListingServer")

@job_mcp.tool()
def search_jobs(keyword: str, location: str, limit: int = 10) -> dict:
    """
    Retrieve open positions that match a keyword and location.

    Parameters
    ----------
    keyword : str
        Role or skill term (e.g., 'data scientist').
    location : str
        City or region filter.
    limit : int, optional
        Maximum jobs to return (default 10).

    Returns
    -------
    dict
        {
            "jobs": [
                {"job_id": <str>, "title": <str>, "company": <str>}, …
            ]
        }
    """
    jobs = [{
        "job_id": uuid.uuid4().hex[:8],
        "title": f"{keyword.title()} {i}",
        "company": f"Company {random.choice('ABCXYZ')}"
    } for i in range(limit)]
    return {"jobs": jobs}


@job_mcp.tool()
def job_detail(job_id: str) -> dict:
    """
    Fetch the full job description.

    Parameters
    ----------
    job_id : str
        Identifier from `search_jobs`.

    Returns
    -------
    dict
        {
            "job_id": <str>,
            "title": <str>,
            "description": <str>,
            "requirements": [<str>, …]
        }
    """
    reqs = ["Python", "SQL", "3+ years experience"]
    return {"job_id": job_id, "title": "Sample Role", "description": "Exciting opportunity …", "requirements": reqs}


if __name__ == "__main__":
    job_mcp.run(transport="stdio")
