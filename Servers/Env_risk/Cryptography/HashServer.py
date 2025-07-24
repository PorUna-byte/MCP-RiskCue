from mcp.server.fastmcp import FastMCP
import hashlib, uuid

hash_mcp = FastMCP("HashServer")

@hash_mcp.tool()
def compute_hash(algorithm: str, data: str) -> dict:
    """
    Compute the message digest of given data.

    Parameters
    ----------
    algorithm : str
        Hash algorithm name, e.g. 'sha256', 'sha512', 'md5'.
    data : str
        Plain-text input to be hashed.

    Returns
    -------
    dict
        {
            "algorithm": <str>,
            "digest_hex": <str>
        }
    """
    h = hashlib.new(algorithm)
    h.update(data.encode())
    return {"algorithm": algorithm, "digest_hex": h.hexdigest()}


@hash_mcp.tool()
def verify_hash(algorithm: str, data: str, expected_hex: str) -> dict:
    """
    Verify that data matches an expected hash value.

    Parameters
    ----------
    algorithm : str
        Hash algorithm used.
    data : str
        Plain-text to verify.
    expected_hex : str
        Reference digest in hexadecimal.

    Returns
    -------
    dict
        {
            "match": <bool>
        }
    """
    actual = compute_hash(algorithm, data)["digest_hex"]
    return {"match": actual.lower() == expected_hex.lower()}


if __name__ == "__main__":
    hash_mcp.run(transport="stdio")
