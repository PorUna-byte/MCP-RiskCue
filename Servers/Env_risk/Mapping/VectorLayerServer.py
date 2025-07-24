from mcp.server.fastmcp import FastMCP
import uuid, random

vec_mcp = FastMCP("VectorLayerServer")

@vec_mcp.tool()
def upload_geojson(name: str, geojson: dict) -> dict:
    """
    Store a GeoJSON feature collection as a map layer.

    Parameters
    ----------
    name : str
        Layer display name.
    geojson : dict
        Raw GeoJSON dict.

    Returns
    -------
    dict
        {"layer_id": <str>, "name": <str>}
    """
    return {"layer_id": uuid.uuid4().hex, "name": name}


@vec_mcp.tool()
def layer_extent(layer_id: str) -> dict:
    """
    Return the bounding box of a vector layer.

    Parameters
    ----------
    layer_id : str

    Returns
    -------
    dict
        {
            "layer_id": <str>,
            "min_lat": <float>,
            "min_lng": <float>,
            "max_lat": <float>,
            "max_lng": <float>
        }
    """
    extent = [random.uniform(-50, 0), random.uniform(-120, -60),
              random.uniform(0, 50), random.uniform(-60, 0)]
    return {"layer_id": layer_id, "min_lat": extent[0], "min_lng": extent[1],
            "max_lat": extent[2], "max_lng": extent[3]}


if __name__ == "__main__":
    vec_mcp.run(transport="stdio")
