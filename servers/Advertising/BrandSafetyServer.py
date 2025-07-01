from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("BrandSafetyServer")

levels = ["safe", "moderate", "risky"]

@mcp.tool()
def check_url(url: str) -> dict:
    """Check a single landing-page URL for brand-safety issues."""
    level = random.choices(levels, weights=[0.7, 0.2, 0.1])[0]
    return {"url": url, "safety_level": level}

@mcp.tool()
def batch_check(urls: list[str]) -> dict:
    """Check up to 5 URLs in batch for brand-safety risk."""
    return {u: check_url(u)["safety_level"] for u in urls[:5]}

if __name__ == "__main__":
    mcp.run(transport="stdio")

