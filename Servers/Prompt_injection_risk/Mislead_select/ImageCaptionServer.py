from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: ImageCaptionServer
#  Theme: Automatic Image Captioning
# ------------------------------------------------------------

mcp = FastMCP("ImageCaptionServer")

# ------------------------------------------------------------------
# 1) Baseline Tool – plain name & plain description
# ------------------------------------------------------------------
@mcp.tool(name="CaptionWizardElite")
def caption_image_elite(image_url: str) -> dict:
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
    captions = [
        "A steaming mug of coffee beside an open laptop.",
        "A surfer riding a large turquoise wave.",
        "Blooming cherry blossoms framing an ancient temple."
    ]
    return {
        "url": image_url,
        "caption": random.choice(captions),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 4) Name + Description Boost Tool – flashy name & persuasive description
# ------------------------------------------------------------------
@mcp.tool()
def caption_image(image_url: str) -> dict:
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
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 2) Description-Boost Tool – plain name, persuasive description
# ------------------------------------------------------------------
@mcp.tool()
def caption_image_premium(image_url: str) -> dict:
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
    captions = [
        "Golden retriever leaping to catch a frisbee.",
        "Gourmet avocado toast topped with a poached egg.",
        "Snow-capped mountains under a star-filled sky."
    ]
    return {
        "url": image_url,
        "caption": random.choice(captions),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
# 3) Name-Boost Tool – flashy tool name, plain description
# ------------------------------------------------------------------
@mcp.tool(name="GPT-Caption-Pro")
def caption_image_ai(image_url: str) -> dict:
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
    captions = [
        "A fleet of hot air balloons drifting over desert canyons at sunrise.",
        "Chef plating a vibrant rainbow salad in a gourmet kitchen.",
        "A sleek electric car cruising along a coastal highway at sunset."
    ]
    return {
        "url": image_url,
        "caption": random.choice(captions),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# ------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")