from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("SalesForecastServer")

@mcp.tool()
def monthly_forecast(product: str, months: int = 3) -> dict:
    """Return a simple sales volume forecast for the next N months."""
    forecast = [random.randint(100, 1000) for _ in range(months)]
    return {"product": product, "monthly_units": forecast}

@mcp.tool()
def probability_to_hit_quota(team: str, target_units: int) -> dict:
    """Return probability (0-1) that a sales team will hit its quota."""
    prob = round(random.uniform(0.3, 0.9), 2)
    return {"team": team, "target_units": target_units, "probability": prob}

if __name__ == "__main__":
    mcp.run(transport="stdio")
