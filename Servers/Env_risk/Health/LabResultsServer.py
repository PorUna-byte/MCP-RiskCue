from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

lab_mcp = FastMCP("LabResultsServer")

@lab_mcp.tool()
def submit_order(patient_id: str, test_code: str) -> dict:
    """
    Place a laboratory test order.

    Parameters
    ----------
    patient_id : str
    test_code  : str  

    Returns
    -------
    dict
        {"order_id": <str>, "expected_ready": <str>}
    """
    ready = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=2)
    return {"order_id": uuid.uuid4().hex, "expected_ready": ready.isoformat() + "Z"}


@lab_mcp.tool()
def result_values(order_id: str) -> dict:
    """
    Fetch finalized numeric results.

    Parameters
    ----------
    order_id : str

    Returns
    -------
    dict
        {"order_id": <str>, "values": {"WBC": <float>, "HGB": <float>, …}}
    """
    values = {"WBC": round(random.uniform(4, 11), 1), "HGB": round(random.uniform(12, 17), 1)}
    return {"order_id": order_id, "values": values}


if __name__ == "__main__":
    lab_mcp.run(transport="stdio")
