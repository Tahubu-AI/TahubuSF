from mcp.server.fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

Sitefinity_Site_Prefix= os.getenv("SITEFINITY_SITE_PREFIX").rstrip("/")  # Configurable URL for Sitefinity site

SFNews  = f"{Sitefinity_Site_Prefix}/api/default/newsitems"
SFBlogs = f"{Sitefinity_Site_Prefix}/api/default/blogs"
SFBlogPosts = f"{Sitefinity_Site_Prefix}/api/default/blogposts"
SFEvents= f"{Sitefinity_Site_Prefix}/api/default/eventsitems"
SFSites = f"{Sitefinity_Site_Prefix}/api/default/sites"
SFLists = f"{Sitefinity_Site_Prefix}/api/default/lists"
SFListItems = f"{Sitefinity_Site_Prefix}/api/default/listitems"
SFSharedContent = f"{Sitefinity_Site_Prefix}/api/default/contentitems"
SFPages = f"{Sitefinity_Site_Prefix}/api/default/pages"
SFPageTemplates = f"{Sitefinity_Site_Prefix}/api/default/templates"

mcp = FastMCP("TahubuSFAPI", port=4000)

@mcp.tool()
async def getNews():
    """
    Get the current news items and Press Releases from the Sitefinity site.

    Returns:
        dict: A dictionary containing the news items and Press Releases:
            - title: str - The title of the news item.
            - summary: str - The summary of the news item.
            - author: str - The Author of the news item.
            - publicationdate: str - The publication date of the news item.
    """
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(SFNews, headers=headers)
        response.raise_for_status()
        data = response.json()
    
    text = ""
    for newsitem in data["value"]:
        title = newsitem["Title"]
        summary = newsitem["Summary"]
        author = newsitem["Author"]
        publicationdate = newsitem["PublicationDate"]
        text += (f"Title: {title}\n Summary: {summary}\n Author: {author}\n Publication Date: {publicationdate}\n\n")   
    return text

@mcp.tool()
async def getBlogPosts():
    """
    Get the current blog posts from the Sitefinity site.
    
    Returns:
        dict: A dictionary containing the blog posts:
            - title: str - The title of the blog post.
            - Summary: str - The summary of the blog post.
            - publicationdate: str - The publication date of the blog post.
    """
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(SFBlogPosts, headers=headers)
        response.raise_for_status()
        data = response.json()
    
    text = ""
    for blogpost in data["value"]:
        title = blogpost["Title"]
        summary = blogpost["Summary"]
        publicationdate = blogpost["PublicationDate"]
        text += (f"Title: {title}\n Summary: {summary}\n Publication Date: {publicationdate}\n\n")   
    return text

@mcp.tool()
async def getPages():
    """
    Get the frontend pages of the Sitefinity site.
    
    Returns:
        dict: A dictionary containing the frontend pages:
            - title: str - The title of the page.
            - urlname: str - The urlname of the page.
            - ishomepage: bool - is the page the home page of the site.
            - publicationdate: str - The publication date of the page.
    """
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(SFPages, headers=headers)
        response.raise_for_status()
        data = response.json()
    
    text = ""
    for page in data["value"]:
        title = page["Title"]
        urlname = page["UrlName"]
        isHomePage = page["IsHomePage"]
        publicationdate = page["PublicationDate"]
        text += (f"Title: {title}\n urlName: {urlname}\n isHomePage: {isHomePage}\n Publication Date: {publicationdate}\n\n")   
    return text

@mcp.tool()
async def getPageTemplates():
    """
    Get the page templates of the Sitefinity site.
    
    Returns:
        dict: A dictionary containing the page templates:
            - title: str - The title of the page template.
            - framework: str - The framework the template is based on.
            - renderer: str - the technology used for the front end.
    """
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(SFPageTemplates, headers=headers)
        response.raise_for_status()
        data = response.json()
    
    text = ""
    for pagetemplate in data["value"]:
        title = pagetemplate["Title"]
        framework = pagetemplate["Framework"]
        renderer = pagetemplate["Renderer"]
        text += (f"Title: {title}\n Framework: {framework}\n Renderer: {renderer}\n\n")   
    return text

@mcp.tool()
async def getSites():
    """
    Get the sites associated with the Sitefinity application.
    
    Returns:
        dict: A dictionary containing the sites associated with the application:
            - name: str - The name of the site variant.
            - liveurl: str - The liveurl of the site variant.
            - isoffline: bool - is the site offline?.
    """
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(SFSites, headers=headers)
        response.raise_for_status()
        data = response.json()
    
    text = ""
    for site in data["value"]:
        name = site["Name"]
        liveurl = site["LiveUrl"]
        isoffline = site["IsOffline"]
        text += (f"Name: {name}\n LiveUrl: {liveurl}\n IsOffline: {isoffline}\n\n")   
    return text

if __name__ == "__main__":
    mcp.run(transport="stdio")
