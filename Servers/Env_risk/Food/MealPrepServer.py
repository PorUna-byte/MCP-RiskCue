from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

prep_mcp = FastMCP("MealPrepServer")

@prep_mcp.tool()
def schedule_prep(user_id: str, date_iso: str, meals: int = 5) -> dict:
    """
    Plan a batch-cooking session.

    Parameters
    ----------
    user_id : str
    date_iso : str
        Scheduled date.
    meals : int, optional
        Number of meal portions (default 5).

    Returns
    -------
    dict
        {
            "prep_id": <str>,
            "date": <str>,
            "meals": <int>
        }
    """
    return {"prep_id": uuid.uuid4().hex, "date": date_iso, "meals": meals}


@prep_mcp.tool()
def prep_status(prep_id: str) -> dict:
    """
    Show estimated completion and current stage.

    Parameters
    ----------
    prep_id : str

    Returns
    -------
    dict
        {
            "prep_id": <str>,
            "stage": <str>, 
            "eta_min": <int>
        }
    """
    stage = random.choice(["planning", "cooking", "cooling", "done"])
    eta = 0 if stage == "done" else random.randint(10, 90)
    return {"prep_id": prep_id, "stage": stage, "eta_min": eta}


if __name__ == "__main__":
    prep_mcp.run(transport="stdio")
