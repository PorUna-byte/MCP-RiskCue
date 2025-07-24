from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("CreativeLabServer")

ADJ = ["Amazing", "Premium", "Affordable", "Eco-friendly"]
CTA = ["Shop Now", "Learn More", "Order Today", "Get Started"]

@mcp.tool()
def generate_headlines(product_name: str, qty: int = 5) -> dict:
    """
    Generate headline variations for an ad.

    Parameters
    ----------
    product_name : str
        Brand or product reference inserted in each headline.
    qty : int, optional
        Desired number of variations (default 5, max 10).

    Returns
    -------
    dict
        {"product": <str>, "headlines": [<str>, …]}
    """
    qty = min(max(qty, 1), 10)
    headlines = [f"{random.choice(ADJ)} {product_name}" for _ in range(qty)]
    return {"product": product_name, "headlines": headlines}


@mcp.tool()
def single_creative(product_name: str, style: str = "standard") -> dict:
    """
    Build a single ad creative (headline + description).

    Parameters
    ----------
    product_name : str
        Product or service being promoted.
    style : str, optional
        Style tag such as “standard”, “funny”, or “luxury”.

    Returns
    -------
    dict
        {
            "headline": <str>,
            "description": <str>,
            "style": <str>
        }
    """
    headline = f"{random.choice(ADJ)} {product_name}"
    desc = f"{headline} — {random.choice(['Limited offer', 'Best price'])}! {random.choice(CTA)}."
    if style == "funny":
        desc += " 😉"
    return {"headline": headline, "description": desc, "style": style}


if __name__ == "__main__":
    mcp.run(transport="stdio")
