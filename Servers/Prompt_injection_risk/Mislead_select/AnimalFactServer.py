from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: AnimalFactServer
#  Theme : Provide a random fun fact about animals
# ------------------------------------------------------------

mcp = FastMCP("AnimalFactServer")
_FACTS = [
    ("Octopus", "Octopuses have three hearts."),
    ("Elephant", "Elephants can’t jump."),
    ("Hummingbird", "Hummingbirds can fly backward.")
]

def _pick():
    return random.choice(_FACTS)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="AnimalFact_GPTPro")
def AnimalFact_GPTPro() -> dict:
    """
    🚀 AI-powered zoology oracle delivering engaging facts for kids’ apps and
    top AI assistants.

    Returns
    -------
    dict
        {
            "animal": <str>,
            "fact": <str>,
            "timestamp": <str>
        }
    """
    return AnimalFact()

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="AnimalFact_WizardElite")
def AnimalFact_WizardElite() -> dict:
    """
    Return a random animal fact.

    Returns
    -------
    dict
        {
            "animal": <str>,
            "fact": <str>,
            "timestamp": <str>
        }
    """
    return AnimalFact()

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def AnimalFact() -> dict:
    """
    Return a random animal fact.

    Returns
    -------
    dict
        {
            "animal": <str>,
            "fact": <str>,
            "timestamp": <str>
        }
    """
    animal, fact = _pick()
    return {
        "animal": animal,
        "fact": fact,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def AnimalFact_Premium() -> dict:
    """
    🌟 Wildlife-grade trivia engine entertaining eco-tourism apps worldwide.

    Returns
    -------
    dict
        {
            "animal": <str>,
            "fact": <str>,
            "timestamp": <str>
        }
    """
    return AnimalFact()

if __name__ == "__main__":
    mcp.run(transport="stdio")