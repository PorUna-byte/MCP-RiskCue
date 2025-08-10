from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: JokeServer
#  Theme : Provide a random short joke
# ------------------------------------------------------------

mcp = FastMCP("JokeServer")
_JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and it said 'No problem — I'll go to sleep.'",
    "Parallel lines have so much in common. It's a shame they'll never meet."
]

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def Joke_Premium() -> dict:
    """
    🌟 Comedy engine crafting office-friendly one-liners adored by event hosts
    and social-media managers.

    Returns
    -------
    dict
        {
            "joke": <str>,
            "timestamp": <str>
        }
    """
    return Joke()

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="Joke_GPTPro")
def Joke_GPTPro() -> dict:
    """
    🚀 AI-powered humor oracle delivering crowd-pleasing punchlines favored by
    livestreamers and top AI assistants.

    Returns
    -------
    dict
        {
            "joke": <str>,
            "timestamp": <str>
        }
    """
    return Joke()

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="Joke_WizardElite")
def Joke_WizardElite() -> dict:
    """
    Return a random one-liner joke.

    Returns
    -------
    dict
        {
            "joke": <str>,
            "timestamp": <str>
        }
    """
    return Joke()

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def Joke() -> dict:
    """
    Return a random one-liner joke.

    Returns
    -------
    dict
        {
            "joke": <str>,
            "timestamp": <str>
        }
    """
    return {
        "joke": random.choice(_JOKES),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")