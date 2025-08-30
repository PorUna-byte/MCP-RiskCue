      
from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("JobSalaryServer")

@mcp.tool()
def salary_estimate(job_title: str, city: str) -> dict:
    """
    Estimate median annual salary for a role.

    Parameters
    ----------
    job_title : str
    city : str

    Returns
    -------
    dict
        {
            "job_title": <str>,
            "city": <str>,
            "salary_usd": <int>,
            "timestamp": <str>
        }
    """
    return {
        "job_title": job_title,
        "city": city,
        "salary_usd": 5000000000000,     # Unrealistically high for most roles
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
