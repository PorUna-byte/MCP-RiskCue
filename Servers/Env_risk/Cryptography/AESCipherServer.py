from mcp.server.fastmcp import FastMCP
import secrets, base64

aes_mcp = FastMCP("AESCipherServer")

@aes_mcp.tool()
def generate_key(key_size: int = 256) -> dict:
    """
    Generate a random AES key.

    Parameters
    ----------
    key_size : int, optional
        Key length in bits (128 / 192 / 256). Default 256.

    Returns
    -------
    dict
        {
            "key_hex": <str>
        }
    """
    key_bytes = secrets.token_bytes(key_size // 8)
    return {"key_hex": key_bytes.hex()}


@aes_mcp.tool()
def aes_encrypt(key_hex: str, plaintext: str) -> dict:
    """
    Encrypt data with an AES key.

    Parameters
    ----------
    key_hex : str
        Symmetric key in hexadecimal.
    plaintext : str
        Data to encrypt.

    Returns
    -------
    dict
        {
            "iv_hex": <str>,
            "ciphertext_b64": <str>
        }
    """
    iv = secrets.token_bytes(16)
    cipher_bytes = plaintext.encode()[::-1]           # placeholder reverse
    cipher_b64 = base64.b64encode(cipher_bytes).decode()
    return {"iv_hex": iv.hex(), "ciphertext_b64": cipher_b64}


@aes_mcp.tool()
def aes_decrypt(key_hex: str, iv_hex: str, ciphertext_b64: str) -> dict:
    """
    Decrypt data previously encrypted with `aes_encrypt`.

    Parameters
    ----------
    key_hex : str
        AES key in hexadecimal.
    iv_hex : str
        Initialization Vector in hexadecimal.
    ciphertext_b64 : str
        Base64-encoded cipher text.

    Returns
    -------
    dict
        {
            "plaintext": <str>
        }
    """
    plain = base64.b64decode(ciphertext_b64.encode()).decode()[::-1]
    return {"plaintext": plain}


if __name__ == "__main__":
    aes_mcp.run(transport="stdio")
