from mcp.server.fastmcp import FastMCP

gap_mcp = FastMCP("SkillGapAnalysisServer")

@gap_mcp.tool()
def compare(job_requirements: list[str], candidate_skills: list[str]) -> dict:
    """
    Highlight missing skills.

    Parameters
    ----------
    job_requirements : list[str]
    candidate_skills : list[str]

    Returns
    -------
    dict
        {"missing": [<str>, …]}
    """
    missing = [req for req in job_requirements if req.lower() not in [s.lower() for s in candidate_skills]]
    return {"missing": missing}


if __name__ == "__main__":
    gap_mcp.run(transport="stdio")
