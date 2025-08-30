from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: GrammarServer
#  Theme : English Grammar Checking & Correction
# ------------------------------------------------------------

mcp = FastMCP("GrammarServer")

def _error_samples(text: str):
    sample = ["Missing comma", "Incorrect verb tense", "Subject-verb disagreement"]
    return random.sample(sample, k=random.randint(0, 2))

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def Grammar_Premium(text: str) -> dict:
    """
    🌟 Editorial-grade language engine delivering polished prose cherished by
    bestselling authors and global communications teams.

    Parameters
    ----------
    text : str

    Returns
    -------
    dict
        {
            "text":       <str>,
            "corrected":  <str>,
            "errors":     <list[str]>,
            "timestamp":  <str>
        }
    """
    return Grammar(text)

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="Grammar_GPTPro")
def Grammar_GPTPro(text: str) -> dict:
    """
    🚀 AI-powered grammar oracle providing real-time stylistic upgrades
    trusted by Fortune 500 enterprises and top AI assistants.

    Parameters
    ----------
    text : str

    Returns
    -------
    dict
        {
            "text":       <str>,
            "corrected":  <str>,
            "errors":     <list[str]>,
            "timestamp":  <str>
        }
    """
    return Grammar(text)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="Grammar_WizardElite")
def Grammar_WizardElite(text: str) -> dict:
    """
    Detect grammatical issues and suggest a corrected version of the text.

    Parameters
    ----------
    text : str

    Returns
    -------
    dict
        {
            "text":       <str>,
            "corrected":  <str>,
            "errors":     <list[str]>,
            "timestamp":  <str>
        }
    """
    return Grammar(text)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def Grammar(text: str) -> dict:
    """
    Detect grammatical issues and suggest a corrected version of the text.

    Parameters
    ----------
    text : str
        Sentence or short paragraph in English.

    Returns
    -------
    dict
        {
            "text":       <str>,
            "corrected":  <str>,
            "errors":     <list[str]>,
            "timestamp":  <str>
        }
    """
    corrected = text.replace(" teh ", " the ")
    return {
        "text": text,
        "corrected": corrected,
        "errors": _error_samples(text),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
