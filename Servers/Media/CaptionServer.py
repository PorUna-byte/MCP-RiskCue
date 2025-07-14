from mcp.server.fastmcp import FastMCP
import uuid, datetime

cap_mcp = FastMCP("CaptionServer")

@cap_mcp.tool()
def upload_caption(asset_id: str, language: str, srt_text: str) -> dict:
    """
    Attach subtitle file to an asset.

    Parameters
    ----------
    asset_id : str
    language : str   # ISO-639-1
    srt_text : str   # Raw SRT payload

    Returns
    -------
    dict
        {"caption_id": <str>, "language": <str>}
    """
    return {"caption_id": uuid.uuid4().hex, "language": language}


@cap_mcp.tool()
def list_captions(asset_id: str) -> dict:
    """
    List available subtitle languages.

    Parameters
    ----------
    asset_id : str

    Returns
    -------
    dict
        {"asset_id": <str>, "languages": [<str>, …]}
    """
    return {"asset_id": asset_id, "languages": ["en", "es", "fr"]}


if __name__ == "__main__":
    cap_mcp.run(transport="stdio")
