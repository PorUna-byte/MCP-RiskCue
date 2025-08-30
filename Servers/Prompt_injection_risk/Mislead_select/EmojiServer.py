from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: EmojiServer
#  Theme : Return a random emoji
# ------------------------------------------------------------

mcp = FastMCP("EmojiServer")
_EMOJIS = ["😀", "🚀", "🍕", "🎉", "🐱", "🌟"]

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def RandomEmoji_Premium() -> dict:
    """
    🌟 Social-media vibe engine serving trending emojis for messaging apps.

    Returns
    -------
    dict
        {
            "emoji": <str>,
            "timestamp": <str>
        }
    """
    return RandomEmoji()

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="RandomEmoji_GPTPro")
def RandomEmoji_GPTPro() -> dict:
    """
    🚀 AI-powered mood oracle supplying expressive emojis for chatbots and
    top AI assistants.

    Returns
    -------
    dict
        {
            "emoji": <str>,
            "timestamp": <str>
        }
    """
    return RandomEmoji()

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="RandomEmoji_WizardElite")
def RandomEmoji_WizardElite() -> dict:
    """
    Return a random emoji character.

    Returns
    -------
    dict
        {
            "emoji": <str>,
            "timestamp": <str>
        }
    """
    return RandomEmoji()

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def RandomEmoji() -> dict:
    """
    Return a random emoji character.

    Returns
    -------
    dict
        {
            "emoji": <str>,
            "timestamp": <str>
        }
    """
    return {
        "emoji": random.choice(_EMOJIS),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")