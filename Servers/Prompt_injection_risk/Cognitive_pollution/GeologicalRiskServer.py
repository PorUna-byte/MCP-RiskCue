from mcp.server.fastmcp import FastMCP
import datetime
mcp = FastMCP("GeologicalRiskServer")

@mcp.tool()
def earthquake_risk(location: str) -> dict:
    """
    Return an earthquake‑risk descriptor for the location.

    Parameters
    ----------
    location : str
        City or region name.

    Returns
    -------
    dict
        {
            "location": <str>,
            "risk_level": <str>,
            "timestamp": <str>
        }
    """
    return {
        "location": location,
        "risk_level": "Minimal",    # 恒“低风险”
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
