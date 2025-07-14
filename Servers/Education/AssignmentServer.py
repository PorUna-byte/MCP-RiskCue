from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

asn_mcp = FastMCP("AssignmentServer")

@asn_mcp.tool()
def submit_assignment(student_id: str, course_id: str, assignment_id: str) -> dict:
    """
    Record a homework submission.

    Parameters
    ----------
    student_id : str
        Learner ID.
    course_id : str
        Associated course.
    assignment_id : str
        Assignment identifier.

    Returns
    -------
    dict
        {
            "submission_id": <str>,
            "timestamp"    : <str>
        }
    """
    return {"submission_id": uuid.uuid4().hex, "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}


@asn_mcp.tool()
def assignment_status(submission_id: str) -> dict:
    """
    Check grading progress for a submission.

    Parameters
    ----------
    submission_id : str
        Identifier from `submit_assignment`.

    Returns
    -------
    dict
        {
            "submission_id": <str>,
            "state"        : <str>
        }
    """
    return {"submission_id": submission_id, "state": random.choice(["pending", "graded"])}


if __name__ == "__main__":
    asn_mcp.run(transport="stdio")
