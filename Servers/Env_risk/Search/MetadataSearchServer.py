from mcp.server.fastmcp import FastMCP
import uuid, random

meta_mcp = FastMCP("MetadataSearchServer")

@meta_mcp.tool()
def search_metadata(field: str, value: str, limit: int = 5) -> dict:
    """
    Query structured metadata records.

    Parameters
    ----------
    field : str
    value : str
    limit : int, optional

    Returns
    -------
    dict
        {
            "field": <str>,
            "value": <str>,
            "records": [
                {"id": <str>, "match_confidence": <float>}, …
            ]
        }
    """
    recs = [{
        "id": uuid.uuid4().hex[:8],
        "match_confidence": round(random.uniform(0.8, 1.0), 2)
    } for _ in range(limit)]
    return {"field": field, "value": value, "records": recs}


if __name__ == "__main__":
    meta_mcp.run(transport="stdio")
