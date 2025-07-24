from mcp.server.fastmcp import FastMCP
import uuid, random

goal_mcp = FastMCP("GoalCoachServer")

@goal_mcp.tool()
def set_goal(user_id: str, description: str, target_date: str) -> dict:
    """
    Define a new fitness goal.

    Parameters
    ----------
    user_id : str
    description : str
    target_date : str

    Returns
    -------
    dict
        {
            "goal_id": <str>,
            "created": <str>
        }
    """
    return {"goal_id": uuid.uuid4().hex, "created": datetime.datetime.utcnow().isoformat() + "Z"}


@goal_mcp.tool()
def goal_progress(goal_id: str) -> dict:
    """
    Estimate percentage completion of a goal.

    Parameters
    ----------
    goal_id : str

    Returns
    -------
    dict
        {
            "goal_id": <str>,
            "progress_pct": <int>
        }
    """
    return {"goal_id": goal_id, "progress_pct": random.randint(0, 100)}


if __name__ == "__main__":
    goal_mcp.run(transport="stdio")
