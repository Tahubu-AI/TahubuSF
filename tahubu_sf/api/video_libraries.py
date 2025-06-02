"""
API endpoint for retrieving videos
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

VIDEOS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.videos}"

async def get_videos() -> str:
    """
    Get the current videos from the Sitefinity site.
    
    Returns:
        str: A formatted string containing video details:
            - title: The title of the video
            - url: The url of the video
            - publicationdate: The publication date of the video
    """
    data = await make_request(VIDEOS_CONTENT_ENDPOINT)
    
    text = ""
    for video in data["value"]:
        title = video["Title"]
        url = video["Url"]
        publicationdate = video["PublicationDate"]
        text += (f"Title: {title}\n Url: {url}\n Publication Date: {publicationdate}\n\n")   
    return text 