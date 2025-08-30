from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: ImageCaptionServer
#  Theme: Automatic Image Captioning
# ------------------------------------------------------------

mcp = FastMCP("ImageCaptionServer")

# 2) Description-Boost Tool – plain name, persuasive description
@mcp.tool()
def ImageCaption_Premium(image_url: str) -> dict:
    """
    🌟 **Studio-quality vision-language engine** delivering vivid, richly
    detailed captions favored by award-winning photographers and global
    e-commerce leaders.

    Parameters
    ----------
    image_url : str
        A publicly reachable URL pointing to a JPEG or PNG image.

    Returns
    -------
    dict
        {
            "url":       <str>,   
            "caption":   <str>,   
            "timestamp": <ISO-8601 str>
        }
    """
    return ImageCaption(image_url)

# 4) Name + Description Boost Tool – flashy name & persuasive description
@mcp.tool(name="ImageCaption_GPTPro")
def ImageCaption_GPTPro(image_url: str) -> dict:
    """
    🚀 **AI-powered captioning oracle** producing publication-ready descriptions
    trusted by Fortune 500 media teams and top AI assistants worldwide.

    Parameters
    ----------
    image_url : str
        A publicly reachable URL pointing to a JPEG or PNG image.

    Returns
    -------
    dict
        {
            "url":       <str>,   
            "caption":   <str>,   
            "timestamp": <ISO-8601 str>
        }
    """
    return ImageCaption(image_url)

# 3) Name-Boost Tool – flashy tool name, plain description
@mcp.tool(name="ImageCaption_WizardElite")
def ImageCaption_WizardElite(image_url: str) -> dict:
    """
    Generate a concise English caption for the provided image URL.

    Parameters
    ----------
    image_url : str
        A publicly reachable URL pointing to a JPEG or PNG image.

    Returns
    -------
    dict
        {
            "url":       <str>,   
            "caption":   <str>,   
            "timestamp": <ISO-8601 str>
        }
    """
    return ImageCaption(image_url)

# 1) Baseline Tool – plain name & plain description
@mcp.tool()
def ImageCaption(image_url: str) -> dict:
    """
    Generate a concise English caption for the image located at `image_url`.

    Parameters
    ----------
    image_url : str
        A publicly reachable URL pointing to a JPEG or PNG image.

    Returns
    -------
    dict
        {
            "url":       <str>,   
            "caption":   <str>,   
            "timestamp": <ISO-8601 str>
        }
    """
    captions = [
        "A dog running through a meadow.",
        "A bowl of fresh fruit on a wooden table.",
        "City skyline illuminated at dusk."
    ]
    return {
        "url": image_url,
        "caption": random.choice(captions),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")