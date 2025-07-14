from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("VoiceCallServer")

@mcp.tool()
def initiate_call(caller: str, callee: str) -> dict:
    """
    Start a voice call and receive a call ID.

    Parameters
    ----------
    caller : str
        Caller’s phone number or user ID.
    callee : str
        Callee’s phone number or user ID.

    Returns
    -------
    dict
        {"caller": <str>, "callee": <str>, "call_id": <str>, "status": <str>}
    """
    call_id = f"CALL{random.randint(10000, 99999)}"
    return {"caller": caller, "callee": callee, "call_id": call_id, "status": "ringing"}


@mcp.tool()
def end_call(call_id: str) -> dict:
    """
    Terminate an active voice call.

    Parameters
    ----------
    call_id : str
        Identifier returned by `initiate_call`.

    Returns
    -------
    dict
        {"call_id": <str>, "duration_sec": <int>, "status": <str>}
    """
    duration = random.randint(5, 3600)
    return {"call_id": call_id, "duration_sec": duration, "status": "ended"}


@mcp.tool()
def call_status(call_id: str) -> dict:
    """
    Query the current status of a call.

    Parameters
    ----------
    call_id : str
        Identifier of the call session.

    Returns
    -------
    dict
        {"call_id": <str>, "status": <str>}
    """
    status = random.choice(["ringing", "in_progress", "ended", "missed"])
    return {"call_id": call_id, "status": status}


if __name__ == "__main__":
    mcp.run(transport="stdio")
