from mcp.server.fastmcp import FastMCP
import uuid, random

grd_mcp = FastMCP("GradebookServer")

@grd_mcp.tool()
def record_grade(student_id: str, course_id: str, item: str, percent: float) -> dict:
    """
    Store or update a grade entry.

    Parameters
    ----------
    student_id : str
        Learner ID.
    course_id : str
        Course context.
    item : str
        Grade item (e.g., 'Midterm').
    percent : float
        Score percentage (0-100).

    Returns
    -------
    dict
        {
            "entry_id": <str>,
            "saved"   : <bool>
        }
    """
    return {"entry_id": uuid.uuid4().hex, "saved": True}


@grd_mcp.tool()
def student_grades(student_id: str, course_id: str) -> dict:
    """
    Retrieve all grade entries for a learner in a course.

    Parameters
    ----------
    student_id : str
        Learner identifier.
    course_id : str
        Course code.

    Returns
    -------
    dict
        {
            "student_id": <str>,
            "course_id" : <str>,
            "grades": [ {"item": <str>, "percent": <float>}, … ]
        }
    """
    items = ["Quiz 1", "Project", "Final"]
    grades = [{"item": itm, "percent": round(random.uniform(60, 100), 1)} for itm in items]
    return {"student_id": student_id, "course_id": course_id, "grades": grades}


if __name__ == "__main__":
    grd_mcp.run(transport="stdio")
