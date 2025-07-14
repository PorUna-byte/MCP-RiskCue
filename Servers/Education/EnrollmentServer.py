from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

enr_mcp = FastMCP("EnrollmentServer")

@enr_mcp.tool()
def enroll_student(student_id: str, course_id: str) -> dict:
    """
    Register a student for a course.

    Parameters
    ----------
    student_id : str
        Learner’s unique ID.
    course_id : str
        Target course identifier.

    Returns
    -------
    dict
        {
            "enrollment_id": <str>,
            "status"       : <str>
        }
    """
    return {"enrollment_id": uuid.uuid4().hex, "status": "enrolled"}


@enr_mcp.tool()
def drop_course(enrollment_id: str) -> dict:
    """
    Unenroll a student from a course.

    Parameters
    ----------
    enrollment_id : str
        Identifier from `enroll_student`.

    Returns
    -------
    dict
        {
            "enrollment_id": <str>,
            "dropped"      : <bool>
        }
    """
    return {"enrollment_id": enrollment_id, "dropped": True}


@enr_mcp.tool()
def list_enrollments(student_id: str) -> dict:
    """
    List all active course registrations for a student.

    Parameters
    ----------
    student_id : str
        Learner ID.

    Returns
    -------
    dict
        {
            "student_id" : <str>,
            "courses"    : [<str>, …]
        }
    """
    courses = [f"CS{random.randint(100, 499)}" for _ in range(random.randint(1, 4))]
    return {"student_id": student_id, "courses": courses}


if __name__ == "__main__":
    enr_mcp.run(transport="stdio")
