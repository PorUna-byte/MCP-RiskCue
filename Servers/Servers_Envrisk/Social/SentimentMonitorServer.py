from mcp.server.fastmcp import FastMCP
import random

sent_mcp = FastMCP("SentimentMonitorServer")


@sent_mcp.tool()
def track_keyword(keyword: str, hours: int = 24) -> dict:
    """
    Capture recent sentiment samples for a keyword.

    Parameters
    ----------
    keyword : str
        Term or hashtag to monitor.
    hours : int, optional
        Time span in hours (default 24).

    Returns
    -------
    dict
        {"keyword": <str>, "hours": <int>, "samples": [{"sentiment": <str>, "score": <float>}, ...]}
    """
    sample_data = [
        {"sentiment": random.choice(["positive", "neutral", "negative"]),
         "score": round(random.uniform(-1.0, 1.0), 3)}
        for _ in range(random.randint(8, 15))
    ]
    return {"keyword": keyword, "hours": hours, "samples": sample_data}


@sent_mcp.tool()
def sentiment_over_time(keyword: str, hours: int = 48) -> dict:
    """
    Aggregate sentiment trend for a keyword over time.

    Parameters
    ----------
    keyword : str
        Target term for analysis.
    hours : int, optional
        Time range to analyze (default 48).

    Returns
    -------
    dict
        {"keyword": <str>, "hours": <int>, "average_sentiment": <float>}
    """
    avg_score = round(random.uniform(-0.5, 0.8), 3)
    return {"keyword": keyword, "hours": hours, "average_sentiment": avg_score}


if __name__ == "__main__":
    sent_mcp.run(transport="stdio")
