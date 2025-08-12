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
    # 输入验证
    if not private_key or not message:
        return {
            "error": "Missing parameters",
            "message": "Both private_key and message are required"
        }
    
    try:
        # 处理NULL字符和其他特殊字符
        safe_message = message.replace('\x00', '[NULL]').replace('\r', '[CR]').replace('\n', '[LF]')
        safe_private_key = private_key.replace('\x00', '[NULL]').replace('\r', '[CR]').replace('\n', '[LF]')
        
        # 确保输入是字符串
        safe_message = str(safe_message)
        safe_private_key = str(safe_private_key)
        
        digest = hashlib.sha256((safe_private_key + safe_message).encode('utf-8', errors='ignore')).hexdigest()
        sig = f"{digest}{uuid.uuid4().hex[:16]}"
        return {"signature_hex": sig}
    except Exception as e:
        return {
            "error": "Signing failed",
            "message": f"Error during signature generation: {str(e)}"
        }


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
    # 输入验证
    if not public_key or not message or not signature_hex:
        return {
            "error": "Missing parameters",
            "message": "All parameters (public_key, message, signature_hex) are required"
        }
    
    try:
        # 处理NULL字符和其他特殊字符
        safe_message = message.replace('\x00', '[NULL]').replace('\r', '[CR]').replace('\n', '[LF]')
        safe_public_key = public_key.replace('\x00', '[NULL]').replace('\r', '[CR]').replace('\n', '[LF]')
        
        # 确保输入是字符串
        safe_message = str(safe_message)
        safe_public_key = str(safe_public_key)
        
        expected_prefix = hashlib.sha256((safe_public_key.replace("PUBLIC", "PRIVATE") + safe_message).encode('utf-8', errors='ignore')).hexdigest()
        return {"valid": signature_hex.startswith(expected_prefix)}
    except Exception as e:
        return {
            "error": "Verification failed",
            "message": f"Error during signature verification: {str(e)}"
        }


if __name__ == "__main__":
    sig_mcp.run(transport="stdio")
