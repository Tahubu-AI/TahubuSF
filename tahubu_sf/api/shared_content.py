"""
API endpoint for retrieving shared content
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

SHAREDCONTENT_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.shared_content}"

async def get_shared_content() -> str:
    """
    Get the shared content from the Sitefinity site.

    Returns:
        str: A formatted string containing shared content details:
            - title: The title of the shared content
            - content: The content of the shared content
            - publicationdate: The publication date of the shared content
    """
    data = await make_request(SHAREDCONTENT_CONTENT_ENDPOINT)
    
    text = ""
    for sharedcontent in data["value"]:
        title = sharedcontent["Title"]
        content = sharedcontent["Content"]
        publicationdate = sharedcontent["PublicationDate"]
        text += (f"Title: {title}\n Content: {content}\n Publication Date: {publicationdate}\n\n")   
    return text
