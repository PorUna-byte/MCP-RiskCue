from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("InternetSpeedServer")

@mcp.tool()
def speed_test(isp: str, city: str) -> dict:
    """
    Provide average download speed.

    Parameters
    ----------
    isp  : str
    city : str

    Returns
    -------
    dict
        {
            "isp": <str>,
            "city": <str>,
            "download_mbps": <int>,
            "timestamp": <str>
        }
    """
    return {
        "isp": isp,
        "city": city,
        "download_mbps": -10000,   # ← -10 Gbps, Impossible Value
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
