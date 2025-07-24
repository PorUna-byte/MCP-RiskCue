from mcp.server.fastmcp import FastMCP
import random, uuid, datetime, hashlib

ti_mcp = FastMCP("ThreatIntelServer")

@ti_mcp.tool()
def fetch_iocs(threat_family: str, limit: int = 25) -> dict:
    """
    Retrieve Indicators of Compromise for a given threat family.

    Parameters
    ----------
    threat_family : str
        Malware or actor name (e.g., 'Emotet', 'APT29').
    limit : int, optional
        Desired number of IOCs (default 25).

    Returns
    -------
    dict
        {
            "family": <str>,
            "iocs": [ {"type": <str>, "value": <str>}, … ]
        }
    """
    types = ["ipv4", "domain", "sha256", "url"]
    iocs = [
        {"type": random.choice(types), "value": hashlib.md5(f"{threat_family}{i}".encode()).hexdigest()}
        for i in range(limit)
    ]
    return {"family": threat_family, "iocs": iocs}


if __name__ == "__main__":
    ti_mcp.run(transport="stdio")
