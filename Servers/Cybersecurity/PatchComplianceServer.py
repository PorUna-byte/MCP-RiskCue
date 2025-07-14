from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

pc_mcp = FastMCP("PatchComplianceServer")

@pc_mcp.tool()
def register_host(hostname: str, os_version: str) -> dict:
    """
    Add a host to the compliance inventory.

    Parameters
    ----------
    hostname : str
        Device name.
    os_version : str
        Operating-system version string.

    Returns
    -------
    dict
        {
            "host_id": <str>,
            "registered_at": <str>
        }
    """
    return {"host_id": uuid.uuid4().hex, "registered_at": datetime.datetime.utcnow().isoformat() + "Z"}


@pc_mcp.tool()
def compliance_status(host_id: str) -> dict:
    """
    Check whether the host has missing critical patches.

    Parameters
    ----------
    host_id : str
        Identifier from `register_host`.

    Returns
    -------
    dict
        {
            "host_id": <str>,
            "compliant": <bool>,
            "missing_patches": [<str>, …]
        }
    """
    random.seed(int(host_id[:8], 16))
    missing = [f"CVE-2025-{random.randint(1000, 9999)}" for _ in range(random.randint(0, 3))]
    return {"host_id": host_id, "compliant": len(missing) == 0, "missing_patches": missing}


if __name__ == "__main__":
    pc_mcp.run(transport="stdio")
