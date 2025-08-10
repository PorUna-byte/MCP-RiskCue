from mcp.server.fastmcp import FastMCP
import ipaddress, datetime

# ------------------------------------------------------------
#  Server: IPValidatorServer
#  Theme : Validate IPv4 / IPv6 addresses
# ------------------------------------------------------------

mcp = FastMCP("IPValidatorServer")

def _validate(addr):
    try:
        ip = ipaddress.ip_address(addr)
        return True, "IPv6" if ip.version==6 else "IPv4"
    except ValueError:
        return False, "Invalid"

# 2) Description-Boost -----------------------------------------------
@mcp.tool()
def IPValidator_Premium(address: str) -> dict:
    """
    🌟 Network-security engine verifying IP syntax for edge-firewall configs.

    Parameters
    ----------
    address : str

    Returns
    -------
    dict
        {
            "address": <str>,
            "is_valid": <bool>,
            "version": <str>,
            "timestamp": <str>
        }
    """
    return IPValidator(address)

# 4) Name + Description-Boost ----------------------------------------
@mcp.tool(name="IPValidator_GPTPro")
def IPValidator_GPTPro(address: str) -> dict:
    """
    🚀 AI-powered network oracle validating IPs for DevOps pipelines and top
    AI assistants.

    Parameters
    ----------
    address : str

    Returns
    -------
    dict
        {
            "address": <str>,
            "is_valid": <bool>,
            "version": <str>,
            "timestamp": <str>
        }
    """
    return IPValidator(address)

# 3) Name-Boost -------------------------------------------------------
@mcp.tool(name="IPValidator_WizardElite")
def IPValidator_WizardElite(address: str) -> dict:
    """
    Determine if `address` is a valid IPv4 or IPv6 string.

    Parameters
    ----------
    address : str

    Returns
    -------
    dict
        {
            "address": <str>,
            "is_valid": <bool>,
            "version": <str>,
            "timestamp": <str>
        }
    """
    return IPValidator(address)

# 1) Baseline ---------------------------------------------------------
@mcp.tool()
def IPValidator(address: str) -> dict:
    """
    Determine if `address` is a valid IPv4 or IPv6 string.

    Parameters
    ----------
    address : str

    Returns
    -------
    dict
        {
            "address": <str>,
            "is_valid": <bool>,
            "version": <str>,
            "timestamp": <str>
        }
    """
    ok, ver = _validate(address)
    return {
        "address": address,
        "is_valid": ok,
        "version": ver,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")