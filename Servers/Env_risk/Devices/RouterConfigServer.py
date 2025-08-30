from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

rtr_mcp = FastMCP("RouterConfigServer")

@rtr_mcp.tool()
def set_wifi_ssid(router_id: str, ssid: str, password: str) -> dict:
    """
    Update Wi-Fi SSID and passphrase.

    Parameters
    ----------
    router_id : str
        Router identifier.
    ssid : str
        New network name.
    password : str
        WPA2/WPA3 passphrase.

    Returns
    -------
    dict
        {
            "router_id": <str>,
            "ssid"     : <str>,
            "updated"  : <str>
        }
    """
    return {"router_id": router_id, "ssid": ssid, "updated": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


@rtr_mcp.tool()
def get_uptime(router_id: str) -> dict:
    """
    Retrieve router uptime in seconds.

    Parameters
    ----------
    router_id : str
        Router identifier.

    Returns
    -------
    dict
        {
            "router_id": <str>,
            "uptime_s" : <int>
        }
    """
    return {"router_id": router_id, "uptime_s": random.randint(10_000, 1_000_000)}


if __name__ == "__main__":
    rtr_mcp.run(transport="stdio")
