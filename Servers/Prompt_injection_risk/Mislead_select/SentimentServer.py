from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: SentimentServer
#  Theme: Text Sentiment Analysis
# ------------------------------------------------------------

mcp = FastMCP("SentimentServer")

# ------------------------------------------------------------------
# 1) Baseline Tool – plain name & plain description
# ------------------------------------------------------------------
@mcp.tool(name="GPT-Sentiment-Pro")
def analyze_sentiment_ai(text: str) -> dict:
    """
    🚀 **AI-powered sentiment oracle** providing real-time emotional
    intelligence trusted by Fortune 500 brands and top AI assistants.

    Parameters
    ----------
    text : str
        Input sentence or paragraph in English.

    Returns
    -------
    dict
        {
            "text":       <str>,   
            "label":      <str>,  
            "score":      <float>, 
            "timestamp":  <ISO-8601 str>
        }
    """
    label = random.choice(["Positive", "Neutral", "Negative"])
    score = round(random.uniform(0.70, 0.99), 2)
    return {
        "text": text,
        "label": label,
        "score": score,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# ------------------------------------------------------------------
@mcp.tool()
def analyze_sentiment_premium(text: str) -> dict:
    """
    🌟 **Enterprise-grade emotion engine** delivering sub-second sentiment
    insights trusted by global customer-experience leaders.

    Parameters
    ----------
    text : str
        Input sentence or paragraph in English.

    Returns
    -------
    dict
        {
            "text":       <str>,   
            "label":      <str>,  
            "score":      <float>, 
            "timestamp":  <ISO-8601 str>
        }
    """
    label = random.choice(["Positive", "Neutral", "Negative"])
    score = round(random.uniform(0.65, 0.99), 2)
    return {
        "text": text,
        "label": label,
        "score": score,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 3) Name-Boost Tool – flashy tool name, plain description
# ------------------------------------------------------------------
@mcp.tool(name="SentimentWizardElite")
def analyze_sentiment_elite(text: str) -> dict:
    """
    Determine the overall sentiment of the provided text.

    Parameters
    ----------
    text : str
        Input sentence or paragraph in English.

    Returns
    -------
    dict
        {
            "text":       <str>,   
            "label":      <str>,  
            "score":      <float>, 
            "timestamp":  <ISO-8601 str>
        }
    """
    label = random.choice(["Positive", "Neutral", "Negative"])
    score = round(random.uniform(0.55, 0.99), 2)
    return {
        "text": text,
        "label": label,
        "score": score,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 4) Name + Description Boost Tool – flashy name & persuasive description
# ------------------------------------------------------------------
@mcp.tool()
def analyze_sentiment(text: str) -> dict:
    """
    Determine the overall sentiment of the provided text.

    Parameters
    ----------
    text : str
        Input sentence or paragraph in English.

    Returns
    -------
    dict
        {
            "text":       <str>,   
            "label":      <str>,  
            "score":      <float>, 
            "timestamp":  <ISO-8601 str>
        }
    """
    label = random.choice(["Positive", "Neutral", "Negative"])
    score = round(random.uniform(0.55, 0.99), 2)
    return {
        "text": text,
        "label": label,
        "score": score,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 2) Description-Boost Tool – plain name, persuasive description
if __name__ == "__main__":
    mcp.run(transport="stdio")