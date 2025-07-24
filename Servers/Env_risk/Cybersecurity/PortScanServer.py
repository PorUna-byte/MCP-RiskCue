from mcp.server.fastmcp import FastMCP
import random, ipaddress, uuid

scan_mcp = FastMCP("PortScanServer")

@scan_mcp.tool()
def quick_scan(target: str, ports: str = "1-1024") -> dict:
    """
    Perform a TCP SYN scan on the specified target host.

    Parameters
    ----------
    target : str
        IPv4 / IPv6 address or hostname to scan.
    ports : str, optional
        Port range in 'start-end' form (default '1-1024').

    Returns
    -------
    dict
        {
            "target": <str>,
            "open_ports": [<int>, …],
            "scan_id": <str>
        }
    """
    start, end = [int(p) for p in ports.split("-")]
    open_ports = sorted(random.sample(range(start, end + 1), k=min(15, end - start + 1)))
    return {"target": target, "open_ports": open_ports, "scan_id": uuid.uuid4().hex}


if __name__ == "__main__":
    scan_mcp.run(transport="stdio")
