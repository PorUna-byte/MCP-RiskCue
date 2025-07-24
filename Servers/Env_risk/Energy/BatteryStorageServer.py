from mcp.server.fastmcp import FastMCP
import random, datetime

bat_mcp = FastMCP("BatteryStorageServer")

@bat_mcp.tool()
def charge_level(site_id: str) -> dict:
    """
    Return current state-of-charge for a BESS asset.

    Parameters
    ----------
    site_id : str
        Battery site identifier.

    Returns
    -------
    dict
        {
            "site_id": <str>,
            "soc_pct": <float>
        }
    """
    return {"site_id": site_id, "soc_pct": round(random.uniform(10, 95), 1)}


@bat_mcp.tool()
def set_charge_target(site_id: str, target_pct: float) -> dict:
    """
    Configure a new SoC target.

    Parameters
    ----------
    site_id : str
        Battery location.
    target_pct : float
        Desired state-of-charge percentage (0-100).

    Returns
    -------
    dict
        {
            "site_id": <str>,
            "accepted": <bool>
        }
    """
    return {"site_id": site_id, "accepted": 0 <= target_pct <= 100}


if __name__ == "__main__":
    bat_mcp.run(transport="stdio")
