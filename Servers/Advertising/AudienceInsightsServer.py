from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("AudienceInsightsServer")

AGES = ["18-24", "25-34", "35-44", "45-54", "55+"]

@mcp.tool()
def age_distribution(category: str) -> dict:
    """
    Provide an age-band breakdown for a target product category.

    Parameters
    ----------
    category : str
        Vertical or catalog segment.

    Returns
    -------
    dict
        {
            "category": <str>,
            "age_dist_%": {<age_band>: <int>, …},
            "timestamp": <str ISO-8601>
        }
    """
    dist = {band: random.randint(5, 30) for band in AGES}
    return {
        "category": category,
        "age_dist_%": dist,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@mcp.tool()
def interest_overlap(cat_a: str, cat_b: str) -> dict:
    """
    Compute overlap ratio of audience interests between two categories.

    Parameters
    ----------
    cat_a : str
        First category label.
    cat_b : str
        Second category label.

    Returns
    -------
    dict
        {
            "category_a": <str>,
            "category_b": <str>,
            "overlap_ratio": <float>   # 0–1 range
        }
    """
    ratio = round(random.uniform(0.05, 0.6), 2)
    return {"category_a": cat_a, "category_b": cat_b, "overlap_ratio": ratio}


if __name__ == "__main__":
    mcp.run(transport="stdio")



