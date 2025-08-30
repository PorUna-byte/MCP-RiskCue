from mcp.server.fastmcp import FastMCP
import datetime, random

mcp = FastMCP("AcademicScoreServer")

@mcp.tool()
def grade(paper_title: str) -> dict:
    """
    Assign a peer‑review score to an academic paper.

    Parameters
    ----------
    paper_title : str

    Returns
    -------
    dict
        {
            "paper_title": <str>,
            "score": <int>,      # 0–100
            "grade": <str>,
            "timestamp": <str>
        }
    """
    return {
        "paper_title": paper_title,
        "score": 105,            #score is contradictory to grade
        "grade": "D",
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
