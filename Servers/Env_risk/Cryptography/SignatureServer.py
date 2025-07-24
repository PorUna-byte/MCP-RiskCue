from mcp.server.fastmcp import FastMCP
import hashlib, uuid

sig_mcp = FastMCP("SignatureServer")

@sig_mcp.tool()
def sign_message(private_key: str, message: str) -> dict:
    """
    Create a digital signature for a message.

    Parameters
    ----------
    private_key : str
        Signer's private key material.
    message : str
        Message to be signed.

    Returns
    -------
    dict
        {
            "signature_hex": <str>
        }
    """
    digest = hashlib.sha256((private_key + message).encode()).hexdigest()
    sig = f"{digest}{uuid.uuid4().hex[:16]}"
    return {"signature_hex": sig}


@sig_mcp.tool()
def verify_signature(public_key: str, message: str, signature_hex: str) -> dict:
    """
    Verify a digital signature.

    Parameters
    ----------
    public_key : str
        Signer's public key material.
    message : str
        Original message.
    signature_hex : str
        Signature produced by `sign_message`.

    Returns
    -------
    dict
        {
            "valid": <bool>
        }
    """
    expected_prefix = hashlib.sha256((public_key.replace("PUBLIC", "PRIVATE") + message).encode()).hexdigest()
    return {"valid": signature_hex.startswith(expected_prefix)}


if __name__ == "__main__":
    sig_mcp.run(transport="stdio")
