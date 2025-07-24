from mcp.server.fastmcp import FastMCP
import uuid, random

plan_mcp = FastMCP("WorkoutPlanServer")

@plan_mcp.tool()
def generate_plan(user_id: str, goal: str, weeks: int = 4) -> dict:
    """
    Produce a multi-week workout schedule for a user.

    Parameters
    ----------
    user_id : str
        Account identifier.
    goal : str
        Primary objective (e.g., 'fat_loss', 'strength').
    weeks : int, optional
        Plan duration (default 4).

    Returns
    -------
    dict
        {
            "plan_id": <str>,
            "weeks"  : <int>,
            "goal"   : <str>
        }
    """
    return {"plan_id": uuid.uuid4().hex, "weeks": weeks, "goal": goal}


@plan_mcp.tool()
def plan_overview(plan_id: str) -> dict:
    """
    Retrieve high-level details of a workout plan.

    Parameters
    ----------
    plan_id : str
        Identifier from `generate_plan`.

    Returns
    -------
    dict
        {
            "plan_id": <str>,
            "sessions": [
                {"day": <str>, "focus": <str>, "duration_min": <int>}, …
            ]
        }
    """
    sessions = [
        {"day": d, "focus": random.choice(["upper", "lower", "cardio"]), "duration_min": random.randint(30, 60)}
        for d in ["Mon", "Tue", "Wed", "Thu", "Fri"]
    ]
    return {"plan_id": plan_id, "sessions": sessions}


if __name__ == "__main__":
    plan_mcp.run(transport="stdio")
