from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

panel_mcp = FastMCP("LabPanelServer")

@panel_mcp.tool()
def order_panel(patient_id: str, panel_code: str) -> dict:
    """
    Submit a bundled laboratory panel (e.g., CMP).

    Parameters
    ----------
    patient_id : str
    panel_code : str

    Returns
    -------
    dict
        {"panel_id": <str>, "expected_ready": <str>}
    """
    ready = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
    return {"panel_id": uuid.uuid4().hex, "expected_ready": ready.isoformat() + "Z"}


@panel_mcp.tool()
def panel_results(panel_id: str) -> dict:
    """
    Retrieve numeric analyte values.

    Parameters
    ----------
    panel_id : str

    Returns
    -------
    dict
        {"panel_id": <str>, "results": {"GLU": <float>, "ALT": <float>, …}}
    """
    vals = {"GLU": round(random.uniform(70, 110), 1), "ALT": round(random.uniform(10, 45), 1)}
    return {"panel_id": panel_id, "results": vals}


if __name__ == "__main__":
    panel_mcp.run(transport="stdio")
