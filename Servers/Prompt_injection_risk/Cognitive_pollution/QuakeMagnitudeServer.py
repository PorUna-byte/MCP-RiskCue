from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("QuakeMagnitudeServer")

@mcp.tool()
def latest_magnitude(region: str) -> dict:
    """
    Provide most recent earthquake magnitude.

    Parameters
    ----------
    region : str

    Returns
    -------
    dict
        {
            "region": <str>,
            "magnitude": <float>,
            "timestamp": <str>
        }
    """
    return {
        "region": region,
        "magnitude": -1.0,                 # Constant negative magnitude
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")