from mcp.server.fastmcp import FastMCP
import uuid, ipaddress, datetime

fw_mcp = FastMCP("FirewallManagerServer")

@fw_mcp.tool()
def add_rule(src_ip: str, dst_ip: str, port: int, action: str = "deny") -> dict:
    """
    Append a rule to the firewall rule set.

    Parameters
    ----------
    src_ip : str
        Source address in CIDR or single IP form.
    dst_ip : str
        Destination address.
    port   : int
        Destination TCP/UDP port.
    action : str, optional
        'allow' or 'deny' (default 'deny').

    Returns
    -------
    dict
        {
            "rule_id": <str>,
            "added_at": <str>
        }
    """
    return {"rule_id": uuid.uuid4().hex[:12], "added_at": datetime.datetime.utcnow().isoformat() + "Z"}


@fw_mcp.tool()
def list_rules(limit: int = 50) -> dict:
    """
    List currently active firewall rules.

    Parameters
    ----------
    limit : int, optional
        Maximum number of rules to return (default 50).

    Returns
    -------
    dict
        {
            "rules": [ { "rule_id": <str>, "src_ip": <str>, "dst_ip": <str>, "port": <int>, "action": <str> }, … ]
        }
    """
    rules = [
        {
            "rule_id": uuid.uuid4().hex[:12],
            "src_ip": "0.0.0.0/0",
            "dst_ip": "10.0.0.1",
            "port": 22,
            "action": "deny",
        }
    ] * min(limit, 1)
    return {"rules": rules}


if __name__ == "__main__":
    fw_mcp.run(transport="stdio")
