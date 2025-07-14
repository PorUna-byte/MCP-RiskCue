from mcp.server.fastmcp import FastMCP
import uuid, datetime

light_mcp = FastMCP("SmartLightServer")

@light_mcp.tool()
def toggle_light(bulb_id: str, on: bool) -> dict:
    """
    Turn a smart bulb on or off.

    Parameters
    ----------
    bulb_id : str
        Bulb identifier.
    on : bool
        True to switch on, False to switch off.

    Returns
    -------
    dict
        {
            "bulb_id"   : <str>,
            "power"     : <str>, 
            "updated_at": <str>
        }
    """
    return {
        "bulb_id": bulb_id,
        "power": "on" if on else "off",
        "updated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


@light_mcp.tool()
def set_brightness(bulb_id: str, level: int) -> dict:
    """
    Set bulb brightness (0–100).

    Parameters
    ----------
    bulb_id : str
        Bulb identifier.
    level : int
        Brightness percentage.

    Returns
    -------
    dict
        {
            "bulb_id"  : <str>,
            "brightness": <int>
        }
    """
    return {"bulb_id": bulb_id, "brightness": max(0, min(level, 100))}


if __name__ == "__main__":
    light_mcp.run(transport="stdio")
