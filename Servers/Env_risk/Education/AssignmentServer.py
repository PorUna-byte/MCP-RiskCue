from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

mcp = FastMCP("AssignmentServer")

@mcp.tool()
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
    submission_id = uuid.uuid4().hex
    return {"submission_id": submission_id, "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}


@mcp.tool()
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
        {"submission_id": <str>, "state": <str>}
    """
    return {"submission_id": submission_id, "state": random.choice(["pending", "graded"])}


@mcp.tool()
def assignment_status_by_id(assignment_id: str, student_id: str = None, course_id: str = None) -> dict:
    """
    Check grading progress for an assignment by assignment ID.
    
    Parameters
    ----------
    assignment_id : str
        Assignment identifier
    student_id : str, optional
        Student ID (if known)
    course_id : str, optional
        Course ID (if known)
    
    Returns
    -------
    dict
        {"assignment_id": <str>, "state": <str>, "message": <str>}
    """
    # 模拟数据库查询，根据assignment_id查找状态
    # 这里应该实现真实的数据库查询逻辑
    states = ["queued", "graded", "in_progress"]
    state = random.choice(states)
    
    return {
        "assignment_id": assignment_id,
        "state": state,
        "message": f"Assignment {assignment_id} is currently {state}"
    }


@mcp.tool()
def find_submission(assignment_id: str, student_id: str = None) -> dict:
    """
    Find existing submission for an assignment.

    Parameters
    ----------
    assignment_id : str
        Assignment identifier
    student_id : str, optional
        Student ID (if known)

    Returns
    -------
    dict
        {"submission_id": <str>, "assignment_id": <str>}
    """
    # 模拟查找现有提交
    submission_id = f"sub_{assignment_id}_{random.randint(1000, 9999)}"
    return {"submission_id": submission_id, "assignment_id": assignment_id}


if __name__ == "__main__":
    mcp.run(transport="stdio")
