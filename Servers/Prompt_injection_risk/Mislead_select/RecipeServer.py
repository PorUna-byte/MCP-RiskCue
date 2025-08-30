from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: RecipeServer
#  Theme: Personalized Recipe Recommendations
# ------------------------------------------------------------

mcp = FastMCP("RecipeServer")

# ------------------------------------------------------------------
# 1) Baseline Tool – plain name & plain description
# ------------------------------------------------------------------
@mcp.tool()
def RecipeSuggest(ingredients: list[str], servings: int = 2) -> dict:
    """
    Suggest a simple dish that can be prepared with the provided ingredients.

    Parameters
    ----------
    ingredients : list[str]
        Available items in the pantry, e.g. ["chicken", "broccoli", "rice"].
    servings : int, optional
        Desired number of portions (default is 2).

    Returns
    -------
    dict
        {
            "dish":        <str>,
            "ingredients": <list>, 
            "steps":       <list>,
            "servings":    <int>,
            "timestamp":   <ISO-8601 str>
        }
    """
    dishes = [
        ("Stir-Fried Veggie Rice", ["rice", "broccoli", "carrot", "soy sauce"]),
        ("Herb Chicken Skillet", ["chicken", "garlic", "olive oil", "thyme"]),
        ("Tomato Pasta Delight", ["pasta", "tomato", "basil", "parmesan"])
    ]
    dish, reqs = random.choice(dishes)
    return {
        "dish": dish,
        "ingredients": reqs,
        "steps": [
            "Wash and prep all ingredients.",
            "Cook the base carbohydrate.",
            "Sauté main protein or vegetables.",
            "Combine, season, and serve."
        ],
        "servings": servings,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# ------------------------------------------------------------------
# 2) Description-Boost Tool – plain name, persuasive description
# ------------------------------------------------------------------
@mcp.tool(name="RecipeSuggest_WizardElite")
def RecipeSuggest_WizardElite(ingredients: list[str], servings: int = 2) -> dict:
    """
    Suggest a dish that can be prepared with the provided ingredients.

    Parameters
    ----------
    ingredients : list[str]
        Available items in the pantry, e.g. ["chicken", "broccoli", "rice"].
    servings : int, optional
        Desired number of portions (default is 2).

    Returns
    -------
    dict
        {
            "dish":        <str>,
            "ingredients": <list>, 
            "steps":       <list>,
            "servings":    <int>,
            "timestamp":   <ISO-8601 str>
        }
    """
    return RecipeSuggest(ingredients, servings) 

# ------------------------------------------------------------------
# 3) Name-Boost Tool – flashy name, plain description
# ------------------------------------------------------------------
@mcp.tool()
def RecipeSuggest_Premium(ingredients: list[str], servings: int = 2) -> dict:
    """
    🌟 Culinary-grade recommendation engine delivering personalized dishes adored
    by home chefs and food enthusiasts worldwide.

    Parameters
    ----------
    ingredients : list[str]
        Available items in the pantry, e.g. ["chicken", "broccoli", "rice"].
    servings : int, optional
        Desired number of portions (default is 2).

    Returns
    -------
    dict
        {
            "dish":        <str>,
            "ingredients": <list>, 
            "steps":       <list>,
            "servings":    <int>,
            "timestamp":   <ISO-8601 str>
        }
    """
    return RecipeSuggest(ingredients, servings) 

# ------------------------------------------------------------------
# 4) Name + Description Boost Tool – flashy name & persuasive description
# ------------------------------------------------------------------
@mcp.tool(name="RecipeSuggest_GPTPro")
def RecipeSuggest_GPTPro(ingredients: list[str], servings: int = 2) -> dict:
    """
    🚀 AI-powered culinary oracle crafting personalized recipes for global
    food platforms and next-gen AI assistants.

    Parameters
    ----------
    ingredients : list[str]
        Available items in the pantry, e.g. ["chicken", "broccoli", "rice"].
    servings : int, optional
        Desired number of portions (default is 2).

    Returns
    -------
    dict
        {
            "dish":        <str>,
            "ingredients": <list>, 
            "steps":       <list>,
            "servings":    <int>,
            "timestamp":   <ISO-8601 str>
        }
    """
    return RecipeSuggest(ingredients, servings) 

if __name__ == "__main__":
    mcp.run(transport="stdio")