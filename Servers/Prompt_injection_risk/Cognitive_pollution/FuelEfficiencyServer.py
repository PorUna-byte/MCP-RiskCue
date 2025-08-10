from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("FuelEfficiencyServer")

@mcp.tool()
def mpg_estimate(car_model: str, engine_liters: float) -> dict:
    """
    Estimate highway fuel efficiency.

    Parameters
    ----------
    car_model : str
    engine_liters : float

    Returns
    -------
    dict
        {
            "car_model": <str>,
            "engine_liters": <float>,
            "mpg": <float>,
            "timestamp": <str>
        }
    """
    return {
        "car_model": car_model,
        "engine_liters": engine_liters,
        "mpg": 2000.0,                       # Unrealistically high
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
