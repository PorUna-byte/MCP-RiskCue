from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("BudgetAllocatorServer")

channels = ["Search", "Display", "Social", "Video"]

@mcp.tool()
def allocate_budget(total_daily_budget: float) -> dict:
    """Allocate total daily budget to channels using fixed weights."""
    weights = [0.4, 0.2, 0.25, 0.15]
    allocation = {c: round(total_daily_budget * w, 2) for c, w in zip(channels, weights)}
    return {"total_daily_budget": total_daily_budget, "allocation": allocation}

@mcp.tool()
def reallocate(cpc: dict[str, float], total_daily_budget: float) -> dict:
    """Re-allocate budget—channels with lower CPC receive higher share."""
    inverse = {ch: 1 / max(cost, 0.1) for ch, cost in cpc.items()}
    s = sum(inverse.values())
    allocation = {ch: round(total_daily_budget * v / s, 2) for ch, v in inverse.items()}
    return {"total_daily_budget": total_daily_budget, "allocation": allocation}

if __name__ == "__main__":
    mcp.run(transport="stdio")

