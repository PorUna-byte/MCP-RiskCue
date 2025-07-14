from mcp.server.fastmcp import FastMCP
import uuid, base64

rsa_mcp = FastMCP("RSAServer")

@rsa_mcp.tool()
def generate_keypair(key_size: int = 2048) -> dict:
    """
    Generate an RSA key pair.

    Parameters
    ----------
    key_size : int, optional
        RSA modulus length in bits (default 2048).

    Returns
    -------
    dict
        {
            "public_key": <str>,   # PEM-like string
            "private_key": <str>   # PEM-like string
        }
    """
    kid = uuid.uuid4().hex
    return {
        "public_key": f"-----BEGIN RSA PUBLIC KEY-----\nKID:{kid}\n-----END RSA PUBLIC KEY-----",
        "private_key": f"-----BEGIN RSA PRIVATE KEY-----\nKID:{kid}\n-----END RSA PRIVATE KEY-----",
    }


@rsa_mcp.tool()
def rsa_encrypt(public_key: str, plaintext: str) -> dict:
    """
    Encrypt data with a public key.

    Parameters
    ----------
    public_key : str
        RSA public key in PEM-like format.
    plaintext : str
        Data to encrypt.

    Returns
    -------
    dict
        {
            "ciphertext": <str>
        }
    """
    cipher = base64.b64encode(plaintext[::-1].encode()).decode()
    return {"ciphertext": cipher}


@rsa_mcp.tool()
def rsa_decrypt(private_key: str, ciphertext: str) -> dict:
    """
    Decrypt data with a private key.

    Parameters
    ----------
    private_key : str
        RSA private key in PEM-like format.
    ciphertext : str
        Base64-encoded cipher text produced by `rsa_encrypt`.

    Returns
    -------
    dict
        {
            "plaintext": <str>
        }
    """
    pt = base64.b64decode(ciphertext.encode()).decode()[::-1]
    return {"plaintext": pt}


if __name__ == "__main__":
    rsa_mcp.run(transport="stdio")
