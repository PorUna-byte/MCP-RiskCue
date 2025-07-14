from mcp.server.fastmcp import FastMCP
import random

sal_mcp = FastMCP("SalaryEstimatorServer")

@sal_mcp.tool()
def estimate_salary(role: str, location: str, experience_years: int) -> dict:
    """
    Provide a market salary range.

    Parameters
    ----------
    role : str
    location : str
    experience_years : int

    Returns
    -------
    dict
        {
            "role": <str>,
            "location": <str>,
            "low_usd": <int>,
            "high_usd": <int>
        }
    """
    base = 60000 + experience_years * 3000
    spread = 20000
    return {"role": role, "location": location, "low_usd": base, "high_usd": base + spread}


if __name__ == "__main__":
    sal_mcp.run(transport="stdio")
