from mcp.server.fastmcp import FastMCP
import uuid, random

ins_mcp = FastMCP("InsuranceEligibilityServer")

@ins_mcp.tool()
def check_coverage(patient_id: str, procedure_code: str) -> dict:
    """
    Verify if a procedure is covered under the patient’s plan.

    Parameters
    ----------
    patient_id : str
    procedure_code : str

    Returns
    -------
    dict
        {"covered": <bool>, "copay_usd": <float>}
    """
    covered = random.random() > 0.1
    copay = 0.0 if not covered else round(random.uniform(10, 50), 2)
    return {"covered": covered, "copay_usd": copay}


if __name__ == "__main__":
    ins_mcp.run(transport="stdio")
