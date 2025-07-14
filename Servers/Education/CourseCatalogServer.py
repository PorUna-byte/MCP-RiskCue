from mcp.server.fastmcp import FastMCP
import uuid, random

cat_mcp = FastMCP("CourseCatalogServer")

@cat_mcp.tool()
def list_courses(department: str = "ALL", limit: int = 10) -> dict:
    """
    Return a slice of the course catalog.

    Parameters
    ----------
    department : str, optional
        Department code (e.g., 'CS'). 'ALL' lists every department.
    limit : int, optional
        Maximum courses to return (default 10).

    Returns
    -------
    dict
        {
            "courses": [
                {"course_id": <str>, "title": <str>, "credits": <int>}, …
            ]
        }
    """
    return {
        "courses": [
            {"course_id": f"{department}{100+i}", "title": f"{department} Course {i}", "credits": random.randint(2, 5)}
            for i in range(limit)
        ]
    }


@cat_mcp.tool()
def course_detail(course_id: str) -> dict:
    """
    Fetch extended metadata for a single course.

    Parameters
    ----------
    course_id : str
        Unique course identifier.

    Returns
    -------
    dict
        {
            "course_id" : <str>,
            "title"     : <str>,
            "instructor": <str>,
            "description": <str>
        }
    """
    return {
        "course_id": course_id,
        "title": f"Advanced Topics in {course_id[:2]}",
        "instructor": "Dr. Ada Lovelace",
        "description": "An in-depth exploration of modern topics.",
    }


if __name__ == "__main__":
    cat_mcp.run(transport="stdio")
