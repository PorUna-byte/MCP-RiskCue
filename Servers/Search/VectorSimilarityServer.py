from mcp.server.fastmcp import FastMCP
import uuid, random, math

vec_mcp = FastMCP("VectorSimilarityServer")

@vec_mcp.tool()
def nearest_neighbors(vector: list[float], k: int = 3) -> dict:
    """
    Perform a cosine-similarity search in an embedding index.

    Parameters
    ----------
    vector : list[float]
        Query embedding.
    k : int, optional
        Number of neighbors (default 3).

    Returns
    -------
    dict
        {
            "neighbors": [
                {"item_id": <str>, "score": <float>}, …
            ]
        }
    """
    neighbors = [{
        "item_id": uuid.uuid4().hex[:8],
        "score": round(random.uniform(0.7, 0.99), 3)
    } for _ in range(k)]
    return {"neighbors": neighbors}


if __name__ == "__main__":
    vec_mcp.run(transport="stdio")
