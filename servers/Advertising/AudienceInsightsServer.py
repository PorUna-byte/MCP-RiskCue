from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("AudienceInsightsServer")

ages = ["18-24", "25-34", "35-44", "45-54", "55+"]
genders = ["male", "female", "other"]
interests = ["Sports", "Tech", "Travel", "Fashion", "Finance", "Gaming"]

@mcp.tool()
def audience_insights(product_category: str) -> dict:
    """Return age and interest distribution (%) for the given category."""
    return {
        "category": product_category,
        "age_dist_%": {a: random.randint(5, 30) for a in ages},
        "interest_dist_%": {i: random.randint(3, 25) for i in interests},
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@mcp.tool()
def gender_breakdown(product_category: str) -> dict:
    """Return gender split (%) for the target audience of a category."""
    male = random.randint(30, 70)
    female = random.randint(20, 100 - male)
    other = 100 - male - female
    return {
        "category": product_category,
        "gender_dist_%": {"male": male, "female": female, "other": other},
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@mcp.tool()
def interest_overlap(cat_a: str, cat_b: str) -> dict:
    """Return an interest-overlap ratio (0–1) between two categories."""
    return {
        "category_a": cat_a,
        "category_b": cat_b,
        "overlap_ratio": round(random.uniform(0.05, 0.6), 2),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")


