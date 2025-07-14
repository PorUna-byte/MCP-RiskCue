from mcp.server.fastmcp import FastMCP
import uuid, random

prd_mcp = FastMCP("ProductSearchServer")

@prd_mcp.tool()
def search_products(term: str, limit: int = 6) -> dict:
    """
    Return catalog items that match a term.

    Parameters
    ----------
    term : str
    limit : int, optional

    Returns
    -------
    dict
        {
            "term": <str>,
            "products": [
                {"sku": <str>, "name": <str>, "price": <float>}, …
            ]
        }
    """
    prods = [{
        "sku": uuid.uuid4().hex[:6],
        "name": f"{term.title()} Item {i}",
        "price": round(random.uniform(5, 200), 2)
    } for i in range(1, limit + 1)]
    return {"term": term, "products": prods}


if __name__ == "__main__":
    prd_mcp.run(transport="stdio")
