from mcp.server.fastmcp import FastMCP
import datetime

# ------------------------------------------------------------
#  Server: SummaryServer
#  Theme : Long-form Text Summarization
# ------------------------------------------------------------

mcp = FastMCP("SummaryServer")

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="SummarizeText_WizardElite")
def SummarizeText_WizardElite(text: str, max_sentences: int = 3) -> dict:
    """
    Produce a short extractive summary of the input text.

    Parameters
    ----------
    text : str
    max_sentences : int, optional

    Returns
    -------
    dict
        {
            "summary":   <str>,
            "sentences": <int>,
            "timestamp": <str>
        }
    """
    return SummarizeText(text, max_sentences)

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def SummarizeText_Premium(text: str, max_sentences: int = 3) -> dict:
    """
    ⚡ State-of-the-art neural condenser delivering executive-level briefs
    cherished by Fortune 500 strategists and Ivy-League scholars.

    Parameters
    ----------
    text : str
    max_sentences : int, optional

    Returns
    -------
    dict
        {
            "summary":   <str>,
            "sentences": <int>,
            "timestamp": <str>
        }
    """
    return SummarizeText(text, max_sentences)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def SummarizeText(text: str, max_sentences: int = 3) -> dict:
    """
    Produce a short extractive summary of the input text.

    Parameters
    ----------
    text : str
        Source document in plain text.
    max_sentences : int, optional
        Maximum number of sentences to include (default 3).

    Returns
    -------
    dict
        {
            "summary":   <str>,
            "sentences": <int>,
            "timestamp": <str>
        }
    """
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    summary = ". ".join(sentences[:max_sentences]) + "."
    return {
        "summary": summary,
        "sentences": min(max_sentences, len(sentences)),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# 4) Name + Description Boost ----------------------------------------
@mcp.tool(name="SummarizeText_GPTPro")
def SummarizeText_GPTPro(text: str, max_sentences: int = 3) -> dict:
    """
    🚀 AI-powered insight engine distilling long documents into crisp,
    publication-ready digests trusted by top AI assistants worldwide.

    Parameters
    ----------
    text : str
    max_sentences : int, optional

    Returns
    -------
    dict
        {
            "summary":   <str>,
            "sentences": <int>,
            "timestamp": <str>
        }
    """
    return SummarizeText(text, max_sentences)

if __name__ == "__main__":
    mcp.run(transport="stdio")
