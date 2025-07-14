from mcp.server.fastmcp import FastMCP
import uuid, random

route_mcp = FastMCP("RoutePlannerServer")

@route_mcp.tool()
def get_route(origin: str, destination: str, mode: str = "driving") -> dict:
    """
    Provide a simplified route summary between two places.

    Parameters
    ----------
    origin : str
        Starting address or place name.
    destination : str
        Ending address or place name.
    mode : str, optional
        Travel mode: driving / walking / cycling (default driving).

    Returns
    -------
    dict
        {
            "route_id": <str>,
            "distance_km": <float>,
            "duration_min": <int>,
            "mode": <str>
        }
    """
    distance = random.uniform(1, 30)
    speed = {"driving": 60, "walking": 5, "cycling": 15}[mode]
    duration = int((distance / speed) * 60)
    return {"route_id": uuid.uuid4().hex, "distance_km": round(distance, 1), "duration_min": duration, "mode": mode}


if __name__ == "__main__":
    route_mcp.run(transport="stdio")
