from mcp.server.fastmcp import FastMCP
import uuid

alg_mcp = FastMCP("AllergyRegistryServer")

@alg_mcp.tool()
def add_allergy(patient_id: str, allergen: str, severity: str) -> dict:
    """
    Record a patient allergy.

    Parameters
    ----------
    patient_id : str
    allergen : str
    severity : str   # mild / moderate / severe

    Returns
    -------
    dict
        {"entry_id": <str>, "stored": <bool>}
    """
    return {"entry_id": uuid.uuid4().hex, "stored": True}


@alg_mcp.tool()
def list_allergies(patient_id: str) -> dict:
    """
    List all known allergies.

    Parameters
    ----------
    patient_id : str

    Returns
    -------
    dict
        {"patient_id": <str>, "allergies": [ {"allergen": <str>, "severity": <str>}, … ]}
    """
    return {"patient_id": patient_id,
            "allergies": [{"allergen": "Penicillin", "severity": "severe"}]}


if __name__ == "__main__":
    alg_mcp.run(transport="stdio")
