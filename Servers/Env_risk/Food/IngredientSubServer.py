from mcp.server.fastmcp import FastMCP
import random

sub_mcp = FastMCP("IngredientSubServer")

@sub_mcp.tool()
def substitute(ingredient: str) -> dict:
    """
    Suggest common alternatives for an ingredient.

    Parameters
    ----------
    ingredient : str
        Ingredient name.

    Returns
    -------
    dict
        {
            "ingredient": <str>,
            "alternatives": [<str>, …]
        }
    """
    alt_pool = {
        "butter": ["ghee", "coconut oil", "olive oil"],
        "sugar": ["honey", "maple syrup", "agave nectar"],
        "egg":   ["flax egg", "chia egg", "applesauce"]
    }
    return {"ingredient": ingredient, "alternatives": alt_pool.get(ingredient.lower(), ["No match found"])}
    

if __name__ == "__main__":
    sub_mcp.run(transport="stdio")
