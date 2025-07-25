"""
API endpoints for retrieving pages and page templates
"""
from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request

# Define the API endpoints for pages and page templates
PAGES_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.pages}"
PAGE_TEMPLATES_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.page_templates}"

async def get_pages() -> str:
    """
    Get the frontend pages of the Sitefinity site.
    
    Returns:
        str: A formatted string containing page details:
            - title: The title of the page
            - urlname: The urlname of the page
            - ishomepage: Whether the page is the home page of the site
            - publicationdate: The publication date of the page
    """
    data = await make_request(PAGES_CONTENT_ENDPOINT)
    
    text = ""
    for page in data["value"]:
        title = page["Title"]
        urlname = page["UrlName"]
        isHomePage = page["IsHomePage"]
        publicationdate = page["PublicationDate"]
        text += (f"Title: {title}\n urlName: {urlname}\n isHomePage: {isHomePage}\n Publication Date: {publicationdate}\n\n")   
    return text

async def get_page_templates() -> str:
    """
    Get the page templates of the Sitefinity site.
    
    Returns:
        str: A formatted string containing page template details:
            - title: The title of the page template
            - framework: The framework the template is based on
            - renderer: The technology used for the front end
    """
    data = await make_request(PAGE_TEMPLATES_CONTENT_ENDPOINT)
    
    text = ""
    for pagetemplate in data["value"]:
        title = pagetemplate["Title"]
        framework = pagetemplate["Framework"]
        renderer = pagetemplate["Renderer"]
        text += (f"Title: {title}\n Framework: {framework}\n Renderer: {renderer}\n\n")   
    return text 