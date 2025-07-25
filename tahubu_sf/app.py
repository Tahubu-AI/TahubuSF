"""
Main application entry point for TahubuSF
"""
import logging
from fastmcp import FastMCP

from tahubu_sf.config.settings import APP_NAME
from tahubu_sf.api.news import get_news, create_news_item
from tahubu_sf.api.blog_posts import create_blog_post, get_parent_blogs, get_blog_posts, get_blog_post_by_id
from tahubu_sf.api.pages import get_pages, get_page_templates
from tahubu_sf.api.sites import get_sites
from tahubu_sf.api.lists import get_list_items
from tahubu_sf.api.list_items import create_list_item, get_parent_lists
from tahubu_sf.api.calendars import get_events
from tahubu_sf.api.events import get_calendars, create_event
from tahubu_sf.api.shared_content import get_shared_content
from tahubu_sf.api.albums import get_images
from tahubu_sf.api.images import create_image, get_albums
from tahubu_sf.api.document_libraries import get_documents
from tahubu_sf.api.documents import create_document, get_document_libraries
from tahubu_sf.api.videos import create_video, get_video_libraries
from tahubu_sf.api.video_libraries import get_videos
from tahubu_sf.api.search_indexes import get_search_indexes
from tahubu_sf.api.taxonomies import get_taxonomies
from tahubu_sf.api.section_presets import get_section_presets
from tahubu_sf.api.forms import get_forms


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
        create_news_item,
        get_blog_posts,
        get_pages,
        get_page_templates,
        get_sites,
        create_blog_post,
        get_parent_blogs,
        get_blog_post_by_id,
        get_list_items,
        create_list_item,
        get_parent_lists,
        get_calendars,
        get_events,
        create_event,
        get_shared_content,
        get_images,
        create_image,
        get_albums,
        get_documents,
        create_document,
        get_document_libraries,
        get_videos,
        create_video,
        get_video_libraries, 
        get_search_indexes,
        get_taxonomies,
        get_section_presets,
        get_forms
    ]
    
    # Register each tool
    for tool_func in tools:
        app.tool()(tool_func)
    
    logger.info(f"{APP_NAME} application created with {len(tools)} tools")
    return app 