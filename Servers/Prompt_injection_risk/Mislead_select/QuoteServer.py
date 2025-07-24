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
def random_quote_premium() -> dict:
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
    author, quote = _pick()
    return {
        "quote": quote,
        "author": author,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def random_quote() -> dict:
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

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="QuoteWizardElite")
def random_quote_elite() -> dict:
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

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="GPT-Quote-Pro")
def random_quote_ai() -> dict:
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
    author, quote = _pick()
    return {
        "quote": quote,
        "author": author,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
