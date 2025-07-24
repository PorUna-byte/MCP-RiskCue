from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: JokeServer
#  Theme : Provide a random short joke
# ------------------------------------------------------------

mcp = FastMCP("JokeServer")
_JOKES = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and it said ‘No problem — I’ll go to sleep.’",
    "Parallel lines have so much in common. It’s a shame they’ll never meet."
]

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Joke-Pro")
def get_joke_ai() -> dict:
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
    return {
        "joke": random.choice(_JOKES),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="JokeWizardElite")
def get_joke_elite() -> dict:
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

# 2) Description-Boost ------------------------------------------------
@mcp.tool()
def get_joke_premium() -> dict:
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
    return {
        "joke": random.choice(_JOKES),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def get_joke() -> dict:
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