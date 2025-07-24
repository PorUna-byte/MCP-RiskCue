from mcp.server.fastmcp import FastMCP
import uuid, random

ref_mcp = FastMCP("ReferralNetworkServer")

@ref_mcp.tool()
def potential_referrers(candidate_id: str, company: str, limit: int = 5) -> dict:
    """
    Suggest employees who could provide a referral.

    Parameters
    ----------
    candidate_id : str
    company : str
    limit : int, optional

    Returns
    -------
    dict
        {
            "employees": [ {"emp_id": <str>, "name": <str>, "mutuals": <int>}, … ]
        }
    """
    emps = [{
        "emp_id": uuid.uuid4().hex[:8],
        "name": f"Employee {i}",
        "mutuals": random.randint(0, 10)
    } for i in range(limit)]
    return {"employees": emps}


@ref_mcp.tool()
def request_referral(emp_id: str, candidate_id: str, job_id: str) -> dict:
    """
    Log a referral request.

    Parameters
    ----------
    emp_id : str
    candidate_id : str
    job_id : str

    Returns
    -------
    dict
        {"request_id": <str>, "sent": <bool>}
    """
    return {"request_id": uuid.uuid4().hex, "sent": True}


if __name__ == "__main__":
    ref_mcp.run(transport="stdio")
