from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("ProjectServer")

@mcp.tool()
def project_status(project_id: str) -> dict:
    """
    Summarize overall status of a project.

    Parameters
    ----------
    project_id : str
        Unique project reference.

    Returns
    -------
    dict
        {
            "project_id": <str>,
            "progress_%": <int>,        # completion percentage
            "health": <str>             # on track / at risk / delayed
        }
    """
    progress = random.randint(5, 95)
    health = random.choice(["on track", "at risk", "delayed"])
    return {"project_id": project_id, "progress_%": progress, "health": health}


@mcp.tool()
def sprint_burndown(project_id: str, days_left: int = 7) -> dict:
    """
    Provide remaining story points for each day of an active sprint.

    Parameters
    ----------
    project_id : str
        Owning project reference.
    days_left : int, optional
        Number of days remaining in the sprint (default 7).

    Returns
    -------
    dict
        {
            "project_id": <str>,
            "days_left": <int>,
            "points_remaining": [<int>, …]   # length = days_left
        }
    """
    days_left = max(1, min(days_left, 14))
    burndown = [random.randint(4, 28) for _ in range(days_left)]
    return {"project_id": project_id, "days_left": days_left, "points_remaining": burndown}


if __name__ == "__main__":
    mcp.run(transport="stdio")
