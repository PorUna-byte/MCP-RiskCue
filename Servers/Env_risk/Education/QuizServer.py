from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

quiz_mcp = FastMCP("QuizServer")

@quiz_mcp.tool()
def start_quiz(student_id: str, quiz_id: str) -> dict:
    """
    Begin a timed quiz session.

    Parameters
    ----------
    student_id : str
        Learner ID.
    quiz_id : str
        Quiz identifier.

    Returns
    -------
    dict
        {
            "session_id": <str>,
            "expires_at": <str>   # ISO-8601
        }
    """
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    return {"session_id": uuid.uuid4().hex, "expires_at": exp.isoformat() + "Z"}


@quiz_mcp.tool()
def submit_answer(session_id: str, question_id: str, answer: str) -> dict:
    """
    Store an answer for a quiz question.

    Parameters
    ----------
    session_id : str
        Quiz session ID.
    question_id : str
        Question identifier.
    answer : str
        Learner’s response.

    Returns
    -------
    dict
        {
            "accepted": <bool>
        }
    """
    return {"accepted": True}


@quiz_mcp.tool()
def quiz_score(session_id: str) -> dict:
    """
    Fetch the final score after submission.

    Parameters
    ----------
    session_id : str
        Quiz session identifier.

    Returns
    -------
    dict
        {
            "session_id": <str>,
            "score_pct" : <float>
        }
    """
    return {"session_id": session_id, "score_pct": round(random.uniform(50, 100), 1)}


if __name__ == "__main__":
    quiz_mcp.run(transport="stdio")
