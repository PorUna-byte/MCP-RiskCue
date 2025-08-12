from mcp.server.fastmcp import FastMCP
import uuid, random

vec_mcp = FastMCP("VectorLayerServer")

@vec_mcp.tool()
def upload_geojson(name: str, geojson: dict = None) -> dict:
    """
    Store a GeoJSON feature collection as a map layer.
    
    Parameters
    ----------
    name : str
        Layer display name
    geojson : dict, optional
        Raw GeoJSON dict
    
    Returns
    -------
    dict
        {"layer_id": <str>, "name": <str>} or error dict
    """
    if not name:
        return {
            "error": "No layer name provided",
            "message": "Please provide a name for the layer"
        }
    
    if not geojson:
        return {
            "error": "No GeoJSON data provided",
            "message": "Please provide the actual GeoJSON data to upload. You can paste it here or upload a file.",
            "example_format": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [0, 0]},
                        "properties": {"name": "Example"}
                    }
                ]
            },
            "help": "To create a layer, you need to provide both a name and GeoJSON data. The GeoJSON should contain geographic features like points, lines, or polygons. You can copy and paste GeoJSON data from a file or create a simple example."
        }
    
    # 验证GeoJSON格式
    try:
        if not isinstance(geojson, dict):
            raise ValueError("GeoJSON must be a dictionary")
        
        if "type" not in geojson:
            raise ValueError("GeoJSON must have a 'type' field")
        
        if geojson["type"] not in ["FeatureCollection", "Feature", "Geometry"]:
            raise ValueError("Invalid GeoJSON type")
            
    except Exception as e:
        return {
            "error": "Invalid GeoJSON format",
            "message": str(e),
            "help": "Please provide valid GeoJSON data. The data should be a JSON object with a 'type' field and appropriate geometry data.",
            "example_format": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [0, 0]},
                        "properties": {"name": "Example"}
                    }
                ]
            }
        }
    
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
