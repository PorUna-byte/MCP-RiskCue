from mcp.server.fastmcp import FastMCP
import uuid, datetime

lab_mcp = FastMCP("PackageLabelServer")

@lab_mcp.tool()
def generate_label(tracking_num: str, service: str = "ground") -> dict:
    """
    Create a printable shipping label.

    Parameters
    ----------
    tracking_num : str
    service : str, optional
        Service level (default 'ground').

    Returns
    -------
    dict
        {"label_id": <str>, "pdf_url": <str>, "created_at": <str>}
    """
    lid = uuid.uuid4().hex
    return {"label_id": lid, "pdf_url": f"https://labels.example.com/{lid}.pdf",
            "created_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z"}


if __name__ == "__main__":
    lab_mcp.run(transport="stdio")
