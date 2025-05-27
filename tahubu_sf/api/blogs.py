"""
API endpoint for retrieving blog posts
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

POSTS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.blog_posts}"

async def get_blog_posts() -> str:
    """
    Get the current blog posts from the Sitefinity site.
    
    Returns:
        str: A formatted string containing blog post details:
            - title: The title of the blog post
            - Summary: The summary of the blog post
            - publicationdate: The publication date of the blog post
    """
    data = await make_request(POSTS_CONTENT_ENDPOINT)
    
    text = ""
    for blogpost in data["value"]:
        title = blogpost["Title"]
        #author = blogpost["CreatedBy"] or "Unknown"
        summary = blogpost["Summary"]
        publicationdate = blogpost["PublicationDate"]
        text += (f"Title: {title}\n Summary: {summary}\n Publication Date: {publicationdate}\nAuthor: {author}\n\n")   
    return text 