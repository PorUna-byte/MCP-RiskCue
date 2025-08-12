from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

rx_mcp = FastMCP("PrescriptionServer")

@rx_mcp.tool()
def prescribe(patient_id: str, drug_name: str, dosage_mg: int, frequency: str) -> dict:
    """
    Generate an electronic prescription.

    Parameters
    ----------
    patient_id : str
    drug_name : str
    dosage_mg : int
    frequency : str   # e.g., 'BID'

    Returns
    -------
    dict
        {"rx_id": <str>, "issued": <str>}
    """
    if not patient_id or not drug_name or not dosage_mg or not frequency:
        return {
            "error": "Missing parameters",
            "message": "All parameters are required: patient_id, drug_name, dosage_mg, and frequency",
            "help": "Please provide all required information: patient ID, drug name, dosage in milligrams, and frequency (e.g., 'BID' for twice daily, 'TID' for three times daily)."
        }
    
    if not isinstance(dosage_mg, int) or dosage_mg <= 0:
        return {
            "error": "Invalid dosage",
            "message": "Dosage must be a positive integer",
            "help": "The dosage_mg parameter must be a positive whole number representing milligrams."
        }
    
    return {"rx_id": uuid.uuid4().hex, "issued": datetime.datetime.utcnow().isoformat() + "Z"}


@rx_mcp.tool()
def refill_status(rx_id: str) -> dict:
    """
    Report next refill eligibility.

    Parameters
    ----------
    rx_id : str

    Returns
    -------
    dict
        {"rx_id": <str>, "next_refill": <str>}
    """
    if not rx_id:
        return {
            "error": "No prescription ID provided",
            "message": "Please provide a valid prescription ID to check refill status",
            "help": "You need to provide a prescription ID to check when the next refill is available."
        }
    
    next_refill = datetime.datetime.utcnow() + datetime.timedelta(days=random.randint(15, 30))
    return {"rx_id": rx_id, "next_refill": next_refill.date().isoformat()}


if __name__ == "__main__":
    rx_mcp.run(transport="stdio")
