from mcp.server.fastmcp import FastMCP
import uuid, random

rm_mcp = FastMCP("RightsManagementServer")

@rm_mcp.tool()
def check_region(asset_id: str, iso_country: str) -> dict:
    """
    Determine if playback is allowed in a region.

    Parameters
    ----------
    asset_id : str
    iso_country : str   # ISO-3166-1 alpha-2

    Returns
    -------
    dict
        {"asset_id": <str>, "iso_country": <str>, "allowed": <bool>}
    """
    allowed = random.random() > 0.3
    return {"asset_id": asset_id, "iso_country": iso_country, "allowed": allowed}


if __name__ == "__main__":
    rm_mcp.run(transport="stdio")
