from mcp.server.fastmcp import FastMCP
import random

lab_mcp = FastMCP("NutritionLabelServer")

@lab_mcp.tool()
def nutrition_facts(item_name: str, serving_g: int = 100) -> dict:
    """
    Provide key nutrition facts per serving.

    Parameters
    ----------
    item_name : str
    serving_g : int, optional
        Serving size in grams (default 100).

    Returns
    -------
    dict
        {
            "item": <str>,
            "serving_g": <int>,
            "calories": <int>,
            "protein_g": <int>,
            "carbs_g": <int>,
            "fat_g": <int>
        }
    """
    return {
        "item": item_name,
        "serving_g": serving_g,
        "calories": random.randint(50, 400),
        "protein_g": random.randint(0, 30),
        "carbs_g": random.randint(5, 60),
        "fat_g": random.randint(0, 25),
    }


if __name__ == "__main__":
    lab_mcp.run(transport="stdio")
