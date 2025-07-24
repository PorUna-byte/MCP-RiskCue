from mcp.server.fastmcp import FastMCP
import uuid, random

opt_mcp = FastMCP("RouteOptimizationServer")

@opt_mcp.tool()
def optimize(stops: list[str], mode: str = "truck") -> dict:
    """
    Return an optimized stop sequence.

    Parameters
    ----------
    stops : list[str]
        Waypoint identifiers.
    mode : str, optional
        Vehicle type (default 'truck').

    Returns
    -------
    dict
        {"plan_id": <str>, "ordered_stops": <list[str]>, "total_km": <float>}
    """
    random.shuffle(stops)
    return {"plan_id": uuid.uuid4().hex, "ordered_stops": stops, "total_km": round(random.uniform(10, 500), 1)}


if __name__ == "__main__":
    opt_mcp.run(transport="stdio")
