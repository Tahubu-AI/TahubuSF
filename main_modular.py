#!/usr/bin/env python
"""
A version of main.py that uses our modular architecture
This file is structured exactly like main.py but uses our modular APIs
"""
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import sys

# Add the project root to the path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Create the server object GLOBALLY - identical to how main.py does it
mcp = FastMCP("TahubuSFAPI")

# Import the tool implementations from our modular architecture
from tahubu_sf.api.news import get_news
from tahubu_sf.api.blogs import get_blog_posts  
from tahubu_sf.api.pages import get_pages, get_page_templates
from tahubu_sf.api.sites import get_sites

# Register tools exactly as they are in main.py
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
    return await get_news()

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
    return await get_blog_posts()

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
    return await get_pages()

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
    return await get_page_templates()

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
    return await get_sites()

if __name__ == "__main__":
    mcp.run(transport="stdio") 