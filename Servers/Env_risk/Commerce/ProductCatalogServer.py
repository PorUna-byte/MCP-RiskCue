from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("ProductCatalogServer")

@mcp.tool()
def get_product(sku: str) -> dict:
    """
    Retrieve core attributes of a product.

    Parameters
    ----------
    sku : str
        Stock-keeping unit used as the primary identifier.

    Returns
    -------
    dict
        {
            "sku": <str>,
            "name": <str>,
            "price_usd": <float>,
            "in_stock": <bool>,
            "timestamp": <ISO-8601 str>
        }
    """
    return {
        "sku": sku,
        "name": f"Product {sku[-4:]}",
        "price_usd": round(random.uniform(5, 180), 2),
        "in_stock": random.choice([True, False]),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }


@mcp.tool()
def search_products(keyword: str, max_results: int = 5) -> dict:
    """
    Search the catalog by keyword and return matching SKUs.

    Parameters
    ----------
    keyword : str
        Search term applied to product titles and descriptions.
    max_results : int, optional
        Maximum number of SKUs to return (default 5).

    Returns
    -------
    dict
        {"keyword": <str>, "results": [<str>, …]}   # list of SKU codes
    """
    skus = [f"SKU{random.randint(10000, 99999)}" for _ in range(max_results)]
    return {"keyword": keyword, "results": skus}


if __name__ == "__main__":
    mcp.run(transport="stdio")
