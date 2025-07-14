from mcp.server.fastmcp import FastMCP
import uuid, random

rec_mcp = FastMCP("RecipeServer")

@rec_mcp.tool()
def search_recipes(keyword: str, limit: int = 5) -> dict:
    """
    Return a short list of recipe titles that match a keyword.

    Parameters
    ----------
    keyword : str
        Ingredient or dish to search for.
    limit : int, optional
        Maximum items to return (default 5).

    Returns
    -------
    dict
        {
            "results": [
                {"recipe_id": <str>, "title": <str>, "ready_min": <int>}, …
            ]
        }
    """
    hits = [
        {"recipe_id": uuid.uuid4().hex[:8],
         "title": f"{keyword.title()} Delight {i}",
         "ready_min": random.randint(15, 60)}
        for i in range(limit)
    ]
    return {"results": hits}


@rec_mcp.tool()
def recipe_detail(recipe_id: str) -> dict:
    """
    Retrieve full ingredient list and instructions.

    Parameters
    ----------
    recipe_id : str
        Identifier from `search_recipes`.

    Returns
    -------
    dict
        {
            "recipe_id"  : <str>,
            "ingredients": [<str>, …],
            "steps"      : [<str>, …]
        }
    """
    ingredients = ["1 cup rice", "200 g chicken", "2 tbsp soy sauce"]
    steps = ["Rinse rice", "Cook chicken", "Combine and season"]
    return {"recipe_id": recipe_id, "ingredients": ingredients, "steps": steps}


if __name__ == "__main__":
    rec_mcp.run(transport="stdio")
