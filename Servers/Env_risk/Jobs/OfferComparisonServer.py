from mcp.server.fastmcp import FastMCP

off_mcp = FastMCP("OfferComparisonServer")

@off_mcp.tool()
def compare_offers(base_usd: list[int], bonus_pct: list[int], equity_usd: list[int]) -> dict:
    """
    Compare up to three job offers.

    Parameters
    ----------
    base_usd : list[int]
        Annual base salaries.
    bonus_pct : list[int]
        Target bonus percentages.
    equity_usd : list[int]
        Year-one equity values.

    Returns
    -------
    dict
        {
            "offers": [
                {"total_comp": <int>, "rank": <int>}, …
            ]
        }
    """
    comps = [b + b*p//100 + e for b, p, e in zip(base_usd, bonus_pct, equity_usd)]
    ranked = sorted([(c, i) for i, c in enumerate(comps)], reverse=True)
    offers = [{"total_comp": c, "rank": r+1} for r, (c, _) in enumerate(ranked)]
    return {"offers": offers}


if __name__ == "__main__":
    off_mcp.run(transport="stdio")
