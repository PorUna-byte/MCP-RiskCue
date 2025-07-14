from mcp.server.fastmcp import FastMCP
import uuid, random

icd_mcp = FastMCP("ICDCodingServer")

@icd_mcp.tool()
def code_lookup(icd10_code: str) -> dict:
    """
    Return a short description for an ICD-10 code.

    Parameters
    ----------
    icd10_code : str

    Returns
    -------
    dict
        {"code": <str>, "description": <str>}
    """
    desc = "Essential (primary) hypertension" if icd10_code.upper() == "I10" else "Unspecified condition"
    return {"code": icd10_code.upper(), "description": desc}


@icd_mcp.tool()
def search_by_text(query: str, limit: int = 5) -> dict:
    """
    Find ICD-10 codes whose descriptions contain a text fragment.

    Parameters
    ----------
    query : str
    limit : int, optional

    Returns
    -------
    dict
        {"matches": [ {"code": <str>, "description": <str>}, … ]}
    """
    matches = [{"code": f"A{random.randint(0,99):02d}", "description": f"{query.title()} Disorder {i}"} for i in range(limit)]
    return {"matches": matches}


if __name__ == "__main__":
    icd_mcp.run(transport="stdio")
