from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("SalesServer")

@mcp.tool()
def monthly_sales_forecast(product: str, months: int = 3) -> dict:
    """
    Forecast unit sales for upcoming months.

    Parameters
    ----------
    product : str
        Product or product-line identifier.
    months : int, optional
        Number of forward months to forecast (default 3, max 12).

    Returns
    -------
    dict
        {
            "product": <str>,
            "forecast_units": [<int>, …]   # length = months
        }
    """
    months = max(1, min(months, 12))
    forecast = [random.randint(120, 1600) for _ in range(months)]
    return {"product": product, "forecast_units": forecast}


@mcp.tool()
def quota_probability(team: str, target_units: int) -> dict:
    """
    Estimate probability that a sales team meets its quota.

    Parameters
    ----------
    team : str
        Sales team name or identifier.
    target_units : int
        Target unit volume for the period.

    Returns
    -------
    dict
        {
            "team": <str>,
            "target_units": <int>,
            "probability": <float>      # 0.0 – 1.0
        }
    """
    prob = round(random.uniform(0.25, 0.95), 2)
    return {"team": team, "target_units": target_units, "probability": prob}


if __name__ == "__main__":
    mcp.run(transport="stdio")
