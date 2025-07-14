from mcp.server.fastmcp import FastMCP
import hashlib, base64

kdf_mcp = FastMCP("KDFServer")

@kdf_mcp.tool()
def derive_key(password: str, salt_b64: str, iterations: int, length: int = 32) -> dict:
    """
    Derive a symmetric key using PBKDF2-HMAC-SHA256.

    Parameters
    ----------
    password : str
        User-supplied secret.
    salt_b64 : str
        Base64-encoded salt.
    iterations : int
        Number of PBKDF2 iterations.
    length : int, optional
        Desired key length in bytes (default 32).

    Returns
    -------
    dict
        {
            "key_hex": <str>
        }
    """
    salt = base64.b64decode(salt_b64.encode())
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen=length)
    return {"key_hex": dk.hex()}


if __name__ == "__main__":
    kdf_mcp.run(transport="stdio")
