from mcp.server.fastmcp import FastMCP
import random, datetime

mcp = FastMCP("MeetingSchedulerServer")

@mcp.tool()
def suggest_meeting_slots(participants: list[str], duration_min: int = 30) -> dict:
    """Return 3 random time slots available for all participants."""
    base_hour = random.randint(9, 15)
    slots = [f"2025-07-0{d} {base_hour+i}:00" for i, d in enumerate([2, 3, 4])]
    return {"participants": participants[:10], "duration_min": duration_min, "suggestions": slots}

if __name__ == "__main__":
    mcp.run(transport="stdio")
