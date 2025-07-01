from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("LandingPageOptimizerServer")

tips = [
    "Add clear CTA above the fold",
    "Compress hero image for faster load",
    "Highlight key benefit in headline",
    "Use trust badges near form",
    "Shorten signup form fields",
]

@mcp.tool()
def lp_recommendations(url: str, max_tips: int = 3) -> dict:
    """Return UX optimization tips for the landing page (random sample)."""
    random.shuffle(tips)
    return {"url": url, "tips": tips[:max_tips]}

@mcp.tool()
def load_speed(url: str) -> dict:
    """Simulate a page-load speed test and grade the result."""
    load_ms = random.randint(800, 4_000)
    return {
        "url": url,
        "load_time_ms": load_ms,
        "grade": "A" if load_ms < 1500 else "B" if load_ms < 2500 else "C",
    }

@mcp.tool()
def ab_test_hint(url: str) -> dict:
    """Suggest an A/B test hypothesis to improve page conversion."""
    hypothesis = random.choice(
        [
            "Changing CTA color may increase CTR",
            "Shorter headline could improve readability",
            "Removing navigation links may lift conversions",
        ]
    )
    return {"url": url, "ab_test_hypothesis": hypothesis}

if __name__ == "__main__":
    mcp.run(transport="stdio")
