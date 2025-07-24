from mcp.server.fastmcp import FastMCP
import uuid, datetime

cert_mcp = FastMCP("CertificateServer")

@cert_mcp.tool()
def issue_certificate(common_name: str, public_key: str) -> dict:
    """
    Issue a simple X.509-like certificate.

    Parameters
    ----------
    common_name : str
        Subject's common name (CN) field.
    public_key : str
        Subject's public key.

    Returns
    -------
    dict
        {
            "serial_number": <str>,
            "issued_at": <str>,
            "expires_at": <str>
        }
    """
    serial = uuid.uuid4().hex.upper()
    now = datetime.datetime.utcnow()
    return {
        "serial_number": serial,
        "issued_at": now.isoformat() + "Z",
        "expires_at": (now + datetime.timedelta(days=365)).isoformat() + "Z",
    }


@cert_mcp.tool()
def revoke_certificate(serial_number: str) -> dict:
    """
    Revoke a previously issued certificate.

    Parameters
    ----------
    serial_number : str
        Certificate serial number.

    Returns
    -------
    dict
        {
            "revoked": <bool>
        }
    """
    return {"revoked": True}


@cert_mcp.tool()
def get_certificate(serial_number: str) -> dict:
    """
    Retrieve certificate metadata.

    Parameters
    ----------
    serial_number : str
        Certificate serial number.

    Returns
    -------
    dict
        {
            "found": <bool>,
            "metadata": <dict | None>
        }
    """
    # Demonstrative fixed response
    return {
        "found": True,
        "metadata": {
            "serial_number": serial_number,
            "common_name": "example.com",
            "issued_at": "2025-01-01T00:00:00Z",
            "expires_at": "2026-01-01T00:00:00Z",
        },
    }


if __name__ == "__main__":
    cert_mcp.run(transport="stdio")
