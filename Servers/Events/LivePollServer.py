from mcp.server.fastmcp import FastMCP
import uuid, random

poll_mcp = FastMCP("LivePollServer")

@poll_mcp.tool()
def create_poll(event_id: str, question: str, options: list[str]) -> dict:
    """
    Launch an in-event poll.

    Parameters
    ----------
    event_id : str
        Parent event.
    question : str
        Poll question text.
    options : list[str]
        List of answer choices.

    Returns
    -------
    dict
        {
            "poll_id": <str>,
            "options": [<str>, …]
        }
    """
    return {"poll_id": uuid.uuid4().hex, "options": options}


@poll_mcp.tool()
def vote(poll_id: str, option_index: int) -> dict:
    """
    Record a vote for an option.

    Parameters
    ----------
    poll_id : str
        Identifier from `create_poll`.
    option_index : int
        Zero-based index of chosen option.

    Returns
    -------
    dict
        {
            "poll_id": <str>,
            "accepted": <bool>
        }
    """
    return {"poll_id": poll_id, "accepted": 0 <= option_index < 10}


@poll_mcp.tool()
def poll_results(poll_id: str) -> dict:
    """
    Retrieve current vote counts.

    Parameters
    ----------
    poll_id : str

    Returns
    -------
    dict
        {
            "poll_id": <str>,
            "results": [<int>, …]
        }
    """
    results = [random.randint(0, 50) for _ in range(random.randint(2, 6))]
    return {"poll_id": poll_id, "results": results}


if __name__ == "__main__":
    poll_mcp.run(transport="stdio")
