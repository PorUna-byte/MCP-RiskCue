from mcp.server.fastmcp import FastMCP
import uuid, random

geo_mcp = FastMCP("GeocodingServer")

@geo_mcp.tool()
def forward_geocode(address: str) -> dict:
    """
    Convert a street address to latitude/longitude.

    Parameters
    ----------
    address : str
        Free-form postal address.

    Returns
    -------
    dict
        {
            "address": <str>,
            "lat": <float>,
            "lng": <float>
        }
    """
    lat = round(random.uniform(-90, 90), 6)
    lng = round(random.uniform(-180, 180), 6)
    return {"address": address, "lat": lat, "lng": lng}


@geo_mcp.tool()
def batch_geocode(addresses: list[str]) -> dict:
    """
    Resolve multiple addresses at once.

    Parameters
    ----------
    addresses : list[str]

    Returns
    -------
    dict
        {
            "results": [ {"address": <str>, "lat": <float>, "lng": <float>}, … ]
        }
    """
    results = [forward_geocode(a) for a in addresses]
    return {"results": results}


if __name__ == "__main__":
    geo_mcp.run(transport="stdio")
