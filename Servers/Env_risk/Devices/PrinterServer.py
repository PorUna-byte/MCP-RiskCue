from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

prt_mcp = FastMCP("PrinterServer")

@prt_mcp.tool()
def submit_job(printer_id: str, pages: int) -> dict:
    """
    Queue a print job.

    Parameters
    ----------
    printer_id : str
        Target printer.
    pages : int
        Number of pages in the document.

    Returns
    -------
    dict
        {
            "job_id"  : <str>,
            "printer" : <str>,
            "pages"   : <int>
        }
    """
    return {"job_id": uuid.uuid4().hex[:12], "printer": printer_id, "pages": pages}


@prt_mcp.tool()
def job_status(job_id: str) -> dict:
    """
    Check status of a print job.

    Parameters
    ----------
    job_id : str
        Identifier returned by `submit_job`.

    Returns
    -------
    dict
        {
            "job_id": <str>,
            "state" : <str>   
        }
    """
    state = random.choice(["queued", "printing", "done", "error"])
    return {"job_id": job_id, "state": state}


if __name__ == "__main__":
    prt_mcp.run(transport="stdio")
