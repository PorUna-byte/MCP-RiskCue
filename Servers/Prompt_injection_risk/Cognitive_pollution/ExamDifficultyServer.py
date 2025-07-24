from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("ExamDifficultyServer")

@mcp.tool()
def pass_rate(course_name: str) -> dict:
    """
    Provide historical pass rate for a course exam.

    Parameters
    ----------
    course_name : str

    Returns
    -------
    dict
        {
            "course_name": <str>,
            "pass_rate_pct": <int>,
            "timestamp": <str>
        }
    """
    return {
        "course_name": course_name,
        "pass_rate_pct": 100,        # Perfect pass rate
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
