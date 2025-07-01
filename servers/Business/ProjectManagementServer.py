from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("ProjectManagementServer")

statuses = ["on track", "at risk", "delayed"]

@mcp.tool()
def project_status(project_id: str) -> dict:
    """Return a health-status summary of a project."""
    progress = random.randint(10, 95)
    status = random.choice(statuses)
    return {"project_id": project_id, "progress_%": progress, "status": status}

@mcp.tool()
def sprint_burndown(project_id: str, days_left: int = 7) -> dict:
    """Return remaining story points per day for the active sprint."""
    burndown = [random.randint(5, 30) for _ in range(days_left)]
    return {"project_id": project_id, "days_left": days_left, "points_remaining": burndown}

if __name__ == "__main__":
    mcp.run(transport="stdio")
