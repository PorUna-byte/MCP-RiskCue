from mcp.server.fastmcp import FastMCP
import random

route_mcp = FastMCP("RoutePlannerServer")


@route_mcp.tool()
def plan_route(origin: str, destination: str, mode: str = "driving") -> dict:
    """
    Generate a route plan between two points.

    Parameters
    ----------
    origin : str
        Starting address or coordinates.
    destination : str
        Destination address or coordinates.
    mode : str, optional
        Travel mode: "driving", "walking", or "cycling" (default "driving").

    Returns
    -------
    dict
        {"origin": <str>, "destination": <str>, "mode": <str>,
         "distance_km": <float>, "duration_min": <int>,
         "route_id": <str>}
    """
    dist = round(random.uniform(2, 50), 2)
    duration = random.randint(5, 120)
    rid = f"RTE{random.randint(10000, 19999)}"
    return {"origin": origin, "destination": destination,
            "mode": mode, "distance_km": dist,
            "duration_min": duration, "route_id": rid}


@route_mcp.tool()
def alternative_routes(origin: str, destination: str, count: int = 3) -> dict:
    """
    Suggest multiple alternative routes.

    Parameters
    ----------
    origin : str
        Starting point.
    destination : str
        Ending point.
    count : int, optional
        Number of alternatives requested (default 3).

    Returns
    -------
    dict
        {"origin": <str>, "destination": <str>,
         "alternatives": [{"route_id": <str>,
                           "distance_km": <float>,
                           "duration_min": <int>}, ...]}
    """
    alts = []
    for _ in range(count):
        alts.append({"route_id": f"ALT{random.randint(20000, 29999)}",
                     "distance_km": round(random.uniform(2, 60), 2),
                     "duration_min": random.randint(6, 140)})
    return {"origin": origin, "destination": destination,
            "alternatives": alts}


if __name__ == "__main__":
    route_mcp.run(transport="stdio")
