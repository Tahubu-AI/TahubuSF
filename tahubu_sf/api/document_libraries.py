"""
API endpoint for retrieving documents
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

DOCUMENTS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.documents}"

async def get_documents() -> str:
    """
    Get the current documents from the Sitefinity site.
    
    Returns:
        str: A formatted string containing blog post details:
            - title: The title of the document
            - extension: The extension of the document
            - url: The URL to access the document
            - publicationdate: The publication date of the blog post
    """
    data = await make_request(DOCUMENTS_CONTENT_ENDPOINT)
    
    text = ""
    for document in data["value"]:
        title = document["Title"]
        extension = document["Extension"]
        url = document["Url"]
        publicationdate = document["PublicationDate"]
        text += (f"Title: {title}\n Extension: {extension}\n Url: {url}\n Publication Date: {publicationdate}\n\n")   
    return text 