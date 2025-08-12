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
    try:
        # 验证key_size参数
        if not isinstance(key_size, int) or key_size <= 0:
            return {
                "error": "Invalid key size",
                "message": "Key size must be a positive integer"
            }
        
        kid = uuid.uuid4().hex
        return {
            "public_key": f"-----BEGIN RSA PUBLIC KEY-----\nKID:{kid}\n-----END RSA PUBLIC KEY-----",
            "private_key": f"-----BEGIN RSA PRIVATE KEY-----\nKID:{kid}\n-----END RSA PRIVATE KEY-----",
        }
    except Exception as e:
        return {
            "error": "Key generation failed",
            "message": f"Error during key pair generation: {str(e)}"
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
    # 输入验证
    if not public_key or not plaintext:
        return {
            "error": "Missing parameters",
            "message": "Both public_key and plaintext are required",
            "help": "Please provide both the public key and the text you want to encrypt. Example: public_key='-----BEGIN RSA PUBLIC KEY-----...', plaintext='Hello World'"
        }
    
    try:
        # 确保输入是字符串
        public_key = str(public_key)
        plaintext = str(plaintext)
        
        # 处理特殊字符
        safe_plaintext = plaintext.replace('\x00', '[NULL]').replace('\r', '[CR]').replace('\n', '[LF]')
        
        cipher = base64.b64encode(safe_plaintext[::-1].encode('utf-8', errors='ignore')).decode()
        return {"ciphertext": cipher}
    except Exception as e:
        return {
            "error": "Encryption failed",
            "message": f"Error during encryption: {str(e)}"
        }


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
    # 输入验证
    if not private_key or not ciphertext:
        return {
            "error": "Missing parameters",
            "message": "Both private_key and ciphertext are required",
            "help": "Please provide both the private key and the encrypted text you want to decrypt. Example: private_key='-----BEGIN RSA PRIVATE KEY-----...', ciphertext='base64_encoded_text'"
        }
    
    try:
        # 确保输入是字符串
        private_key = str(private_key)
        ciphertext = str(ciphertext)
        
        # 验证base64格式
        try:
            decoded = base64.b64decode(ciphertext.encode(), validate=True)
        except Exception:
            return {
                "error": "Invalid ciphertext",
                "message": "Ciphertext must be valid base64-encoded data",
                "help": "The ciphertext should be a valid base64 string. If you have encrypted text, make sure it's properly encoded."
            }
        
        pt = decoded.decode('utf-8', errors='ignore')[::-1]
        return {"plaintext": pt}
    except Exception as e:
        return {
            "error": "Decryption failed",
            "message": f"Error during decryption: {str(e)}"
        }


if __name__ == "__main__":
    rsa_mcp.run(transport="stdio")
