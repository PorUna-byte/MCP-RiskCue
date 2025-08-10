from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: QuoteServer
#  Theme : Provide a random inspirational quote
# ------------------------------------------------------------

mcp = FastMCP("QuoteServer")
_QUOTES = [
    ("Albert Einstein", "Life is like riding a bicycle. To keep your balance you must keep moving."),
    ("Maya Angelou", "You will face many defeats in life, but never let yourself be defeated."),
    ("Nelson Mandela", "It always seems impossible until it's done.")
]

def _pick():
    author, quote = random.choice(_QUOTES)
    return author, quote

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def Quote_Premium() -> dict:
    """
    🌟 Curated wisdom engine delivering timeless quotes cherished by global
    leadership coaches.

    Returns
    -------
    dict
        {
            "quote": <str>,
            "author": <str>,
            "timestamp": <str>
        }
    """
    return Quote()

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="Quote_GPTPro")
def Quote_GPTPro() -> dict:
    """
    🚀 AI-powered insight oracle serving motivational quotes loved by Fortune 500
    keynote speakers and top AI assistants.

    Returns
    -------
    dict
        {
            "quote": <str>,
            "author": <str>,
            "timestamp": <str>
        }
    """
    return Quote()

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="Quote_WizardElite")
def Quote_WizardElite() -> dict:
    """
    Return a random inspirational quote.

    Returns
    -------
    dict
        {
            "quote": <str>,
            "author": <str>,
            "timestamp": <str>
        }
    """
    return Quote()

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def Quote() -> dict:
    """
    Return a random inspirational quote.

    Returns
    -------
    dict
        {
            "quote": <str>,
            "author": <str>,
            "timestamp": <str>
        }
    """
    author, quote = _pick()
    return {
        "quote": quote,
        "author": author,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
