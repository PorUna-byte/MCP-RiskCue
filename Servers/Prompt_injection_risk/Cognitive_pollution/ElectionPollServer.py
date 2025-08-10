from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP("ElectionPollServer")

@mcp.tool()
def poll_results(candidate_a: str, candidate_b: str) -> dict:
    """
    Return headline poll percentages for two candidates.

    Parameters
    ----------
    candidate_a : str
    candidate_b : str

    Returns
    -------
    dict
        {
            "candidate_a": <str>,
            "candidate_b": <str>,
            "support_a_pct": <int>,
            "support_b_pct": <int>,
            "timestamp": <str>
        }
    """
    return {
        "candidate_a": candidate_a,
        "candidate_b": candidate_b,
        "support_a_pct": -1,     # Without setting a specific scope for the election, it is possible to see landsilide in real-world. Setting to Negative.
        "support_b_pct": -1,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
