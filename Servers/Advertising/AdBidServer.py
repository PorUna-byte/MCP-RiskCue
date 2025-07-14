from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("AdBidServer")

@mcp.tool()
def recommend_bid(keyword: str, region: str = "national") -> dict:
    """
    Recommend a cost-per-click bid for a given keyword.

    Parameters
    ----------
    keyword : str
        Search term to be purchased.
    region : str, optional
        Geographic market (default “national”).

    Returns
    -------
    dict
        {
            "keyword": <str>,             # echoed keyword
            "region": <str>,              # echoed region
            "suggested_bid": <float>,     # recommended bid in CNY
            "timestamp": <str ISO-8601>   # generation time
        }
    """
    base = random.uniform(2.0, 6.0)
    multiplier = 1.3 if region.lower() in {"beijing", "shanghai"} else 1.0
    return {
        "keyword": keyword,
        "region": region,
        "suggested_bid": round(base * multiplier, 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@mcp.tool()
def keyword_competition(keyword: str) -> dict:
    """
    Estimate how competitive a keyword is.

    Parameters
    ----------
    keyword : str
        Search term to evaluate.

    Returns
    -------
    dict
        {
            "keyword": <str>,
            "competition_score": <int>,   # 0–100 scale, higher = tougher
            "band": <str>                 # Low / Medium / High
        }
    """
    score = random.randint(10, 95)
    band = "High" if score > 70 else "Medium" if score > 40 else "Low"
    return {"keyword": keyword, "competition_score": score, "band": band}


if __name__ == "__main__":
    mcp.run(transport="stdio")


