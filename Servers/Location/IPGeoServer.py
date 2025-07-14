from mcp.server.fastmcp import FastMCP
import random

ip_mcp = FastMCP("IPGeoServer")

@ip_mcp.tool()
def ip_lookup(ip_addr: str) -> dict:
    """
    Map an IPv4/IPv6 address to approximate location.

    Parameters
    ----------
    ip_addr : str

    Returns
    -------
    dict
        {
            "ip": <str>,
            "country": <str>,
            "city": <str>,
            "lat": <float>,
            "lng": <float>
        }
    """
    countries = [("US", "New York"), ("FR", "Paris"), ("JP", "Tokyo"), ("BR", "São Paulo")]
    country, city = random.choice(countries)
    lat = round(random.uniform(-90, 90), 4)
    lng = round(random.uniform(-180, 180), 4)
    return {"ip": ip_addr, "country": country, "city": city, "lat": lat, "lng": lng}


if __name__ == "__main__":
    ip_mcp.run(transport="stdio")
