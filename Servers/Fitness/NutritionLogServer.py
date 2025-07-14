from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

nut_mcp = FastMCP("NutritionLogServer")

@nut_mcp.tool()
def add_meal(user_id: str, name: str, calories: int, protein_g: int, carbs_g: int, fat_g: int) -> dict:
    """
    Record a meal with macro nutrients.

    Parameters
    ----------
    user_id : str
    name : str
    calories : int
    protein_g : int
    carbs_g : int
    fat_g : int

    Returns
    -------
    dict
        {
            "meal_id": <str>,
            "timestamp": <str>
        }
    """
    return {"meal_id": uuid.uuid4().hex, "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}


@nut_mcp.tool()
def daily_macros(user_id: str, date_iso: str) -> dict:
    """
    Aggregate macros for the specified day.

    Parameters
    ----------
    user_id : str
    date_iso : str

    Returns
    -------
    dict
        {
            "date": <str>,
            "calories": <int>,
            "protein_g": <int>,
            "carbs_g": <int>,
            "fat_g": <int>
        }
    """
    return {
        "date": date_iso,
        "calories": random.randint(1500, 3000),
        "protein_g": random.randint(80, 180),
        "carbs_g": random.randint(150, 350),
        "fat_g": random.randint(40, 90),
    }


if __name__ == "__main__":
    nut_mcp.run(transport="stdio")
