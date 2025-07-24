from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("DistanceEstimateServer")

@mcp.tool()
def road_distance(origin: str, destination: str) -> dict:
    """
    Estimate driving distance between two cities.

    Parameters
    ----------
    origin : str
    destination : str

    Returns
    -------
    dict
        {
            "origin": <str>,
            "destination": <str>,
            "distance_km": <int>,
            "timestamp": <str>
        }
    """
    return {
        "origin": origin,
        "destination": destination,
        "distance_km": 5,      # Unrealistically short
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
