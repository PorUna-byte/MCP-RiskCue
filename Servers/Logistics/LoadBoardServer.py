from mcp.server.fastmcp import FastMCP
import uuid, random

load_mcp = FastMCP("LoadBoardServer")

@load_mcp.tool()
def post_load(origin: str, destination: str, weight_kg: float) -> dict:
    """
    Add a freight load to the board.

    Parameters
    ----------
    origin : str
    destination : str
    weight_kg : float

    Returns
    -------
    dict
        {"load_id": <str>, "posted": <bool>}
    """
    return {"load_id": uuid.uuid4().hex, "posted": True}


@load_mcp.tool()
def search_loads(origin: str, radius_km: int = 100, limit: int = 5) -> dict:
    """
    Find loads near a city.

    Parameters
    ----------
    origin : str
    radius_km : int, optional
    limit : int, optional

    Returns
    -------
    dict
        {"loads": [ {"load_id": <str>, "dest": <str>, "weight_kg": <float>}, … ]}
    """
    loads = [{
        "load_id": uuid.uuid4().hex[:8],
        "dest": f"City {i}",
        "weight_kg": round(random.uniform(1000, 20000), 1)
    } for i in range(limit)]
    return {"loads": loads}


if __name__ == "__main__":
    load_mcp.run(transport="stdio")
