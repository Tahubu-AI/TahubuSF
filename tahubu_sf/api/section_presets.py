"""
API endpoint for retrieving Section Presets
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

SECTIONPRESETS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.section_presets}"

async def get_section_presets() -> str:
    """
    Get the current section presets from the Sitefinity site.

    Returns:
        str: A formatted string containing news item details:
            - title: The title of the section preset
            - thumbnail: the thumbnail url of the section preset
    """
    data = await make_request(SECTIONPRESETS_CONTENT_ENDPOINT)
    
    text = ""
    for sectionpreset in data["value"]:
        title = sectionpreset["Title"]
        thumbnail = sectionpreset["Thumbnail"]
        text += (f"Title: {title}\n Thumbnail: {thumbnail}\n\n")   
    return text
