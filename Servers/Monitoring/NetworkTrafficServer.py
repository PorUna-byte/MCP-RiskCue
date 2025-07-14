from mcp.server.fastmcp import FastMCP
import random, datetime

net_mcp = FastMCP("NetworkTrafficServer")

@net_mcp.tool()
def interface_stats(interface: str) -> dict:
    """
    Report RX/TX throughput in Mbps.

    Parameters
    ----------
    interface : str

    Returns
    -------
    dict
        {"interface": <str>, "rx_mbps": <float>, "tx_mbps": <float>}
    """
    return {"interface": interface,
            "rx_mbps": round(random.uniform(0, 1000), 2),
            "tx_mbps": round(random.uniform(0, 1000), 2)}


if __name__ == "__main__":
    net_mcp.run(transport="stdio")
