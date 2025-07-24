from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("BrandSafetyServer")

LEVELS = ["safe", "moderate", "risky"]

@mcp.tool()
def check_page(url: str) -> dict:
    """
    Evaluate a landing page for brand-safety compliance.

    Parameters
    ----------
    url : str
        Fully-qualified landing page URL.

    Returns
    -------
    dict
        {"url": <str>, "safety_level": <str>}   # safe / moderate / risky
    """
    level = random.choices(LEVELS, weights=[0.7, 0.2, 0.1])[0]
    return {"url": url, "safety_level": level}


@mcp.tool()
def batch_check(urls: list[str]) -> dict:
    """
    Inspect up to five URLs for brand-safety status.

    Parameters
    ----------
    urls : list[str]
        Collection of landing page URLs (max 5).

    Returns
    -------
    dict
        {<url>: <safety_level>, …}
    """
    subset = urls[:5]
    return {u: check_page(u)["safety_level"] for u in subset}


if __name__ == "__main__":
    mcp.run(transport="stdio")
