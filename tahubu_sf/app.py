"""
Main application entry point for TahubuSF
"""
import logging
from mcp.server.fastmcp import FastMCP

from tahubu_sf.config.settings import APP_NAME
from tahubu_sf.api.news import get_news
from tahubu_sf.api.blogs import get_blog_posts
from tahubu_sf.api.blog_posts import create_blog_post_draft, get_parent_blogs
from tahubu_sf.api.pages import get_pages, get_page_templates
from tahubu_sf.api.sites import get_sites

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def create_app() -> FastMCP:
    """
    Create and configure the MCP application
    
    Returns:
        FastMCP: The configured application
    """
    logger.info(f"Creating {APP_NAME} application")
    app = FastMCP(APP_NAME)
    
    # Register API tools
    tools = [
        get_news,
        get_blog_posts,
        get_pages,
        get_page_templates,
        get_sites,
        create_blog_post_draft,
        get_parent_blogs
    ]
    
    # Register each tool
    for tool_func in tools:
        app.tool()(tool_func)
    
    logger.info(f"{APP_NAME} application created with {len(tools)} tools")
    return app 