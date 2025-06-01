"""
API endpoint for retrieving images
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

IMAGES_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.images}"

async def get_images() -> str:
    """
    Get the current images from the Sitefinity site.
    
    Returns:
        str: A formatted string containing image details:
            - title: The title of the list item
            - embedurl: The embed url of the image
            - publicationdate: The publication date of the image
            - extension: The file extension of the image
            - totalsize: The total size of the image in bytes
            - width: The width of the image in pixels
            - height: The height of the image in pixels
            - alternativetext: The alternative text for the image
    """
    data = await make_request(IMAGES_CONTENT_ENDPOINT)
    
    text = ""
    for image in data["value"]:
        title = image["Title"]
        embedurl = image["EmbedUrl"]
        extension = image["Extension"]
        totalsize = image["TotalSize"]
        width = image["Width"]
        height = image["Height"]
        alternativetext = image["AlternativeText"]
        publicationdate = image["PublicationDate"]
        text += (f"Title: {title}\n EmbedUrl: {embedurl}\n Publication Date: {publicationdate}\n Extension: {extension}\n Total Size: {totalsize}\n Width: {width}\n Height: {height}\n Alternative Text: {alternativetext}\n\n")   
    return text 