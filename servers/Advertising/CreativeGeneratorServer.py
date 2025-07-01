from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("CreativeGeneratorServer")

adjectives = ["Amazing", "Innovative", "Affordable", "Premium", "Eco-friendly"]
cta = ["Shop Now", "Learn More", "Order Today", "Get Started", "Try Free"]

@mcp.tool()
def generate_creative(product_name: str, tone: str = "positive") -> dict:
    """Generate a single ad title & description for the product."""
    title = f"{random.choice(adjectives)} {product_name}"
    desc = (
        f"{title} — {random.choice(['limited offer', 'best price', 'new arrival'])}! "
        f"{random.choice(cta)}."
    )
    if tone == "funny":
        desc += " 😉"
    return {"title": title, "description": desc}

@mcp.tool()
def headline_variations(product_name: str, n: int = 5) -> dict:
    """Generate multiple headline variations for testing."""
    variations = [
        f"{random.choice(adjectives)} {product_name}" for _ in range(min(n, 10))
    ]
    return {"headlines": variations}

if __name__ == "__main__":
    mcp.run(transport="stdio")


