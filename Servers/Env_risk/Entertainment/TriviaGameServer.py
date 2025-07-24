from mcp.server.fastmcp import FastMCP
import uuid, random, datetime

triv_mcp = FastMCP("TriviaGameServer")

@triv_mcp.tool()
def start_game(player: str) -> dict:
    """
    Begin a new trivia round.

    Parameters
    ----------
    player : str
        Player handle.

    Returns
    -------
    dict
        {
            "game_id"   : <str>,
            "started_at": <str>
        }
    """
    return {"game_id": uuid.uuid4().hex, "started_at": datetime.datetime.utcnow().isoformat() + "Z"}


@triv_mcp.tool()
def submit_answer(game_id: str, question_num: int, answer: str) -> dict:
    """
    Record an answer to a trivia question.

    Parameters
    ----------
    game_id : str
        Identifier from `start_game`.
    question_num : int
        Question index (starting at 1).
    answer : str
        Player’s response.

    Returns
    -------
    dict
        {
            "correct": <bool>
        }
    """
    return {"correct": random.random() > 0.5}


@triv_mcp.tool()
def get_score(game_id: str) -> dict:
    """
    Fetch cumulative score.

    Parameters
    ----------
    game_id : str

    Returns
    -------
    dict
        {
            "game_id": <str>,
            "points" : <int>
        }
    """
    return {"game_id": game_id, "points": random.randint(0, 10)}


if __name__ == "__main__":
    triv_mcp.run(transport="stdio")
