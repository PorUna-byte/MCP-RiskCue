from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("ProductCatalogServer")

@mcp.tool()
def get_product(sku: str) -> dict:
    """Return basic product details for the given SKU."""
    return {
        "sku": sku,
        "name": f"Product {sku[-4:]}",
        "price_usd": round(random.uniform(5, 150), 2),
        "in_stock": random.choice([True, False]),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@mcp.tool()
def search_products(keyword: str, max_results: int = 5) -> dict:
    """Return a list of SKUs that match the search keyword."""
    skus = [f"SKU{random.randint(10000, 99999)}" for _ in range(max_results)]
    return {"keyword": keyword, "results": skus}

if __name__ == "__main__":
    mcp.run(transport="stdio")
