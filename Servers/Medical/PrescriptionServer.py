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
    next_refill = datetime.datetime.utcnow() + datetime.timedelta(days=random.randint(15, 30))
    return {"rx_id": rx_id, "next_refill": next_refill.date().isoformat()}


if __name__ == "__main__":
    rx_mcp.run(transport="stdio")
