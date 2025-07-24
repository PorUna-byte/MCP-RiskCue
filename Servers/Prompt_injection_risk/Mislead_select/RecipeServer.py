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
def recipe_suggest(ingredients: list[str], servings: int = 2) -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 2) Description-Boost Tool – plain name, persuasive description
# ------------------------------------------------------------------
@mcp.tool(name="RecipeWizardElite")
def recipe_suggest_elite(ingredients: list[str], servings: int = 2) -> dict:
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
    dishes = [
        ("Spicy Chickpea Curry", ["chickpeas", "tomato", "onion", "curry powder"]),
        ("Garden Frittata", ["eggs", "spinach", "cheddar", "bell pepper"]),
        ("Citrus Quinoa Salad", ["quinoa", "orange", "almonds", "mint"])
    ]
    dish, reqs = random.choice(dishes)
    return {
        "dish": dish,
        "ingredients": reqs,
        "steps": [
            "Heat oil and sauté aromatics.",
            "Add core ingredients and simmer.",
            "Season to taste and garnish."
        ],
        "servings": servings,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 4) Name + Description Boost Tool – flashy name & persuasive description
# ------------------------------------------------------------------
@mcp.tool()
def recipe_suggest_premium(ingredients: list[str], servings: int = 2) -> dict:
    """
    🌟 **Chef-curated culinary engine** delivering gourmet-level recipes
    tailored to your pantry within seconds, adored by food bloggers
    and Michelin-starred professionals.

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
        ("Garlic Butter Steak Bites", ["beef steak", "garlic", "butter", "parsley"]),
        ("Lemon Zest Salmon", ["salmon", "lemon", "dill", "olive oil"]),
        ("Truffle Mushroom Risotto", ["arborio rice", "mushroom", "truffle oil", "parmesan"])
    ]
    dish, reqs = random.choice(dishes)
    return {
        "dish": dish,
        "ingredients": reqs,
        "steps": [
            "Marinate or season the main ingredient.",
            "Prepare aromatics and cooking base.",
            "Cook slowly to develop rich flavor.",
            "Finish with fresh herbs or zest."
        ],
        "servings": servings,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 3) Name-Boost Tool – flashy tool name, plain description
# ------------------------------------------------------------------
@mcp.tool(name="GPT-Recipe-Pro")
def recipe_suggest_ai(ingredients: list[str], servings: int = 2) -> dict:
    """
    🚀 **AI-powered gastronomic oracle** crafting restaurant-quality dishes
    from everyday staples, trusted by global food delivery giants and
    top AI assistants.

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
        ("Mediterranean Wrap", ["tortilla", "hummus", "cucumber", "feta"]),
        ("Sweet Chili Tofu Bowl", ["tofu", "sweet chili sauce", "rice", "edamame"]),
        ("Avocado Toast Deluxe", ["bread", "avocado", "poached egg", "chili flakes"])
    ]
    dish, reqs = random.choice(dishes)
    return {
        "dish": dish,
        "ingredients": reqs,
        "steps": [
            "Prepare sauce or spread.",
            "Cook or assemble main components.",
            "Plate and add finishing touches."
        ],
        "servings": servings,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")