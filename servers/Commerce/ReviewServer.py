from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("ReviewServer")

@mcp.tool()
def get_reviews(sku: str, max_results: int = 3) -> dict:
    """Return a list of textual reviews for the product."""
    reviews = [f"Review {i+1} for {sku}" for i in range(max_results)]
    return {"sku": sku, "reviews": reviews}

@mcp.tool()
def average_rating(sku: str) -> dict:
    """Return a average rating (1-5 stars) for the product."""
    rating = round(random.uniform(2.5, 5.0), 1)
    return {"sku": sku, "avg_rating": rating}

if __name__ == "__main__":
    mcp.run(transport="stdio")
