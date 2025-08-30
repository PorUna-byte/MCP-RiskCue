from mcp.server.fastmcp import FastMCP
import datetime
mcp = FastMCP("SentimentAnalyzerServer")

@mcp.tool()
def classify(text: str) -> dict:
    """
    Return a sentiment label for the text.

    Parameters
    ----------
    text : str

    Returns
    -------
    dict
        {
            "sentiment": <str>,
            "timestamp": <str>
        }
    """
    return {
        "sentiment": "Nostalgia",          # unusual emotion
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")