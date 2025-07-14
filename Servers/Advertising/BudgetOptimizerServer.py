from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("BudgetOptimizerServer")

CHANNELS = ["Search", "Display", "Social", "Video"]

@mcp.tool()
def allocate_daily(total_budget: float) -> dict:
    """
    Distribute a daily budget across standard channels.

    Parameters
    ----------
    total_budget : float
        Total spend allowed for the day (CNY).

    Returns
    -------
    dict
        {"total_budget": <float>, "allocation": {<channel>: <float>, …}}
    """
    weights = [0.4, 0.2, 0.25, 0.15]
    allocation = {ch: round(total_budget * w, 2) for ch, w in zip(CHANNELS, weights)}
    return {"total_budget": total_budget, "allocation": allocation}


@mcp.tool()
def reallocate_by_cpc(cpc_map: dict[str, float], total_budget: float) -> dict:
    """
    Re-balance budget toward lower-CPC channels.

    Parameters
    ----------
    cpc_map : dict[str, float]
        Observed cost-per-click for each channel.
    total_budget : float
        Daily spend ceiling (CNY).

    Returns
    -------
    dict
        {"total_budget": <float>, "allocation": {<channel>: <float>, …}}
    """
    inverse = {ch: 1 / max(cost, 0.1) for ch, cost in cpc_map.items()}
    s = sum(inverse.values())
    allocation = {ch: round(total_budget * v / s, 2) for ch, v in inverse.items()}
    return {"total_budget": total_budget, "allocation": allocation}


if __name__ == "__main__":
    mcp.run(transport="stdio")
