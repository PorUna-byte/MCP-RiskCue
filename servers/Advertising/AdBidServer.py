from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("AdBidServer")

@mcp.tool()
def recommend_bid(keyword: str, region: str = "national") -> dict:
    """Return a bid (CNY) suggestion for a single keyword in the given region."""
    base = random.uniform(2.0, 6.0)
    multiplier = 1.3 if region.lower() in {"beijing", "shanghai"} else 1.0
    return {
        "keyword": keyword,
        "region": region,
        "suggested_bid": round(base * multiplier, 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@mcp.tool()
def bulk_recommend(keywords: list[str], region: str = "national") -> dict:
    """Return bid suggestions for a batch of keywords (max 5)."""
    return {kw: recommend_bid(kw, region)["suggested_bid"] for kw in keywords[:5]}

@mcp.tool()
def keyword_competition(keyword: str) -> dict:
    """Estimate how competitive a keyword is on a 0–100 scale."""
    score = random.randint(10, 95)
    return {
        "keyword": keyword,
        "competition_score": score,
        "category": "High" if score > 70 else "Medium" if score > 40 else "Low",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")

