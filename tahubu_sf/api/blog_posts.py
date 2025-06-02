"""
API endpoints for creating and managing blog posts
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional

from tahubu_sf.config.settings import ENDPOINTS, CONTENT_TYPES
from tahubu_sf.utils.http import make_request, make_post_request
from tahubu_sf.utils import generate_url_name

logger = logging.getLogger(__name__)

BLOGS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.blogs}"
POSTS_CONTENT_ENDPOINT = f"{ENDPOINTS.content}/{CONTENT_TYPES.blog_posts}"
POSTS_MANAGEMENT_ENDPOINT = f"{ENDPOINTS.management}/{CONTENT_TYPES.blog_posts}"

async def create_blog_post(
    title: str,
    content: str,
    parent_id: str,
    summary: Optional[str] = None,
    allow_comments: bool = True,
    draft: bool = True,
) -> Dict[str, Any]:
    """
    Create a new blog post as a draft in Sitefinity.
    
    Args:
        title: The title of the blog post
        content: The main content of the blog post (HTML supported)
        parent_id: The ID of the parent blog (REQUIRED)
        summary: A short summary of the blog post (optional)
        allow_comments: Whether to allow comments on the post (default: True)
        draft: Whether to create the post as a draft (default: True)
    
    Returns:
        Dict[str, Any]: Response from the Sitefinity API, including the created post's ID
    """
    try:
        logger.info(f"Creating blog post draft with title: {title}")
        
        # Validate required parameters
        if not parent_id:
            raise ValueError("Parent blog ID (parent_id) is required for creating blog posts")
        
        # Create a timestamp for the current time
        now = datetime.utcnow().isoformat() + "Z"
        
        # Prepare the blog post data
        post_data = {
            "Title": title,
            "Content": content,
            "Summary": summary or "",
            "PublicationDate": now,
            "AllowComments": allow_comments,
            "IncludeInSitemap": True,
            "ParentId": parent_id,
        }
        
        # Generate a proper URL name from the title following Sitefinity requirements
        url_name = generate_url_name(title)
        
        post_data["UrlName"] = url_name
        
        logger.debug(f"Generated URL name: {url_name}")

        endpoint = POSTS_MANAGEMENT_ENDPOINT if draft else POSTS_CONTENT_ENDPOINT
        
        # Send POST request to create the blog post
        response = await make_post_request(endpoint, post_data)
        
        logger.info(f"Blog post draft created successfully: {response.get('Id', 'unknown ID')}")
        return response
    except Exception as e:
        logger.error(f"Error creating blog post draft: {str(e)}")
        raise Exception(f"Failed to create blog post draft: {str(e)}") from e

async def get_parent_blogs() -> Dict[str, str]:
    """
    Get a list of available parent blogs for selection.
    
    Returns:
        Dict[str, str]: Dictionary of blog IDs and their titles
    """
    try:
        data = await make_request(BLOGS_CONTENT_ENDPOINT)
        blogs = {blog["Id"]: blog["Title"] for blog in data.get("value", [])}
        logger.info(f"Found {len(blogs)} parent blogs")
        return blogs
    except Exception as e:
        logger.error(f"Error retrieving parent blogs: {str(e)}")
        return {} 