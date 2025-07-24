from mcp.server.fastmcp import FastMCP
import random

net_mcp = FastMCP("NetworkUtilityServer")


@net_mcp.tool()
def dns_lookup(hostname: str) -> dict:
    """
    Resolve a hostname to an IP address.

    Parameters
    ----------
    hostname : str
        Domain name (e.g., "example.com").

    Returns
    -------
    dict
        {"hostname": <str>, "ip": <str>}
    """
    fake_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    return {"hostname": hostname, "ip": fake_ip}


@net_mcp.tool()
def port_check(host: str, port: int) -> dict:
    """
    Check if a TCP port is reachable.

    Parameters
    ----------
    host : str
        Target host.
    port : int
        TCP port number.

    Returns
    -------
    dict
        {"host": <str>, "port": <int>, "reachable": <bool>}
    """
    reachable = random.choice([True, False])
    return {"host": host, "port": port, "reachable": reachable}


if __name__ == "__main__":
    net_mcp.run(transport="stdio")
