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
def random_emoji_premium() -> dict:
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
    return random_emoji()

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="GPT-Emoji-Pro")
def random_emoji_ai() -> dict:
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
    return random_emoji()

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="EmojiWizardElite")
def random_emoji_elite() -> dict:
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
    return random_emoji()

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def random_emoji() -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")