"""
API endpoint for retrieving List Items
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

POSTS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.list_items}"

async def get_list_items() -> str:
    """
    Get the current list items from the Sitefinity site.
    
    Returns:
        str: A formatted string containing list item details:
            - title: The title of the list item
            - content: The content of the list item
            - publicationdate: The publication date of the blog post
    """
    data = await make_request(POSTS_CONTENT_ENDPOINT)
    
    text = ""
    for listitem in data["value"]:
        title = listitem["Title"]
        content = listitem["Content"]
        publicationdate = listitem["PublicationDate"]
        text += (f"Title: {title}\n Content: {content}\n Publication Date: {publicationdate}\n\n")   
    return text 