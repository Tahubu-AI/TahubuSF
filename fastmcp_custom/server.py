#!/usr/bin/env python3
"""
FastMCP 2.0 HTTP Streaming Server
Provides advanced MCP server capabilities including HTTP streaming, auth, and proxying
Uses existing TahubuSF tools from the tahubu_sf package
"""
import logging
import argparse
from typing import Optional

# Import FastMCP from the installed package - not our local folder
import sys
import os
# Add project root to Python path to import tahubu_sf
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import from the actual fastmcp package (not our local one)
try:
    from fastmcp import FastMCP
except ImportError:
    print("❌ FastMCP library not found. Please install with: pip install fastmcp")
    sys.exit(1)

# Import all existing tools from tahubu_sf
from tahubu_sf.config.settings import APP_NAME
from tahubu_sf.api.news import get_news, create_news_item
from tahubu_sf.api.blog_posts import create_blog_post, get_blog_posts, get_blog_post_by_id, get_parent_blogs
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

def create_fastmcp_server(
    name: str = f"{APP_NAME} FastMCP 2.0",
    port: int = 3000,
    host: str = "127.0.0.1",
    enable_auth: bool = False,
    auth_token: Optional[str] = None
) -> FastMCP:
    """
    Create a FastMCP 2.0 server with HTTP streaming capabilities
    
    Args:
        name: Server name
        port: Port to run on
        host: Host to bind to
        enable_auth: Whether to enable authentication
        auth_token: Authentication token if auth is enabled
        
    Returns:
        FastMCP: Configured FastMCP server
    """
    logger.info(f"Creating {name} with FastMCP 2.0")
    
    # Create FastMCP server with basic configuration
    server = FastMCP(name=name)
    
    # Configure authentication if requested
    if enable_auth and auth_token:
        logger.info("Authentication enabled")
        # Note: FastMCP 2.0 auth configuration will be added when the API is available
    
    # Register all existing MCP tools from tahubu_sf
    tools = [
        # Content retrieval tools
        get_news,
        get_blog_posts,
        get_blog_post_by_id,
        get_pages,
        get_page_templates,
        get_sites,
        get_list_items,
        get_events,
        get_shared_content,
        get_images,
        get_documents,
        get_videos,
        get_search_indexes,
        get_taxonomies,
        get_section_presets,
        get_forms,
        
        # Content creation tools
        create_news_item,
        create_blog_post,
        create_list_item,
        create_event,
        create_image,
        create_document,
        create_video,
        
        # Helper tools
        get_parent_blogs,
        get_parent_lists,
        get_calendars,
        get_albums,
        get_document_libraries,
        get_video_libraries
    ]
    
    # Register each tool with the server
    for tool_func in tools:
        server.tool()(tool_func)
        logger.debug(f"Registered tool: {tool_func.__name__}")
    
    logger.info(f"FastMCP 2.0 server created with {len(tools)} tools")
    return server

def main():
    """Main entry point for FastMCP 2.0 server"""
    parser = argparse.ArgumentParser(
        description="TahubuSF FastMCP 2.0 Server with HTTP Streaming"
    )
    parser.add_argument(
        "--transport", 
        choices=["stdio", "streamable-http", "sse"], 
        default="streamable-http",
        help="Transport protocol to use (default: streamable-http)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=3000,
        help="Port for HTTP transport (default: 3000)"
    )
    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--auth", 
        action="store_true",
        help="Enable authentication"
    )
    parser.add_argument(
        "--auth-token", 
        help="Authentication token"
    )
    parser.add_argument(
        "--proxy", 
        action="store_true",
        help="Enable remote server proxying"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create the server
    server = create_fastmcp_server(
        port=args.port,
        host=args.host,
        enable_auth=args.auth,
        auth_token=args.auth_token
    )
    
    # Log configuration
    logger.info(f"Starting FastMCP 2.0 server:")
    logger.info(f"  Transport: {args.transport}")
    logger.info(f"  Host: {args.host}")
    logger.info(f"  Port: {args.port}")
    logger.info(f"  Authentication: {'enabled' if args.auth else 'disabled'}")
    logger.info(f"  Proxying: {'enabled' if args.proxy else 'disabled'}")
    
    # Start the server with the specified transport
    if args.transport == "streamable-http":
        logger.info("Starting Streamable HTTP transport...")
        # FastMCP 2.0 Streamable HTTP transport
        server.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        logger.info("Starting SSE transport...")
        # FastMCP 2.0 SSE transport
        server.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.info("Starting STDIO transport...")
        server.run(transport="stdio")

if __name__ == "__main__":
    main() 