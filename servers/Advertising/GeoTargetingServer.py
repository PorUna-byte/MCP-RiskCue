from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("GeoTargetingServer")

cities = ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Hangzhou", "Chengdu"]

@mcp.tool()
def suggest_geo_targets(product_category: str, top_k: int = 3) -> dict:
    """Suggest top cities for better ROI in the given category."""
    random.shuffle(cities)
    return {"category": product_category, "cities": cities[:top_k]}

@mcp.tool()
def top_provinces(product_category: str, top_k: int = 3) -> dict:
    """Return provinces with highest CVR for the category."""
    provinces = ["Guangdong", "Zhejiang", "Jiangsu", "Sichuan", "Shandong"]
    random.shuffle(provinces)
    cvr = {p: round(random.uniform(1.5, 4.0), 2) for p in provinces[:top_k]}
    return {"category": product_category, "province_cvr_%": cvr}

if __name__ == "__main__":
    mcp.run(transport="stdio")

