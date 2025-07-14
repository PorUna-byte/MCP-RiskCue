from mcp.server.fastmcp import FastMCP
import uuid, random

cus_mcp = FastMCP("CustomsDocServer")

@cus_mcp.tool()
def generate_invoice(shipment_id: str, value_usd: float, country_dest: str) -> dict:
    """
    Produce a commercial invoice for export.

    Parameters
    ----------
    shipment_id : str
    value_usd : float
    country_dest : str

    Returns
    -------
    dict
        {"doc_id": <str>, "hs_code": <str>}
    """
    hs = random.choice(["8471.30", "9503.00", "4202.92"])
    return {"doc_id": uuid.uuid4().hex, "hs_code": hs}


if __name__ == "__main__":
    cus_mcp.run(transport="stdio")
