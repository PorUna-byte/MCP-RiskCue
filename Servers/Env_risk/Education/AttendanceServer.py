from mcp.server.fastmcp import FastMCP
import uuid, datetime, random

att_mcp = FastMCP("AttendanceServer")

@att_mcp.tool()
def mark_attendance(student_id: str, course_id: str, date_iso: str) -> dict:
    """
    Mark a student present for a specific class meeting.

    Parameters
    ----------
    student_id : str
        Learner ID.
    course_id : str
        Course identifier.
    date_iso : str
        Class date in ISO format (YYYY-MM-DD).

    Returns
    -------
    dict
        {
            "record_id": <str>,
            "marked"   : <bool>
        }
    """
    return {"record_id": uuid.uuid4().hex, "marked": True}


@att_mcp.tool()
def attendance_report(course_id: str, date_iso: str) -> dict:
    """
    Summarize attendance for a given session.

    Parameters
    ----------
    course_id : str
        Course code.
    date_iso : str
        Session date.

    Returns
    -------
    dict
        {
            "course_id": <str>,
            "date"     : <str>,
            "present"  : <int>,
            "absent"   : <int>
        }
    """
    present = random.randint(10, 30)
    total = 35
    return {"course_id": course_id, "date": date_iso, "present": present, "absent": total - present}


if __name__ == "__main__":
    att_mcp.run(transport="stdio")
