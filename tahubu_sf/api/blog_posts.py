"""
API endpoints for creating and managing blog posts
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional

from tahubu_sf.config.settings import ENDPOINTS
from tahubu_sf.utils.http import make_request, make_post_request

logger = logging.getLogger(__name__)

async def create_blog_post_draft(
    title: str,
    content: str,
    parent_id: str,
    summary: Optional[str] = None,
    allow_comments: bool = True,
) -> Dict[str, Any]:
    """
    Create a new blog post as a draft in Sitefinity.
    
    Args:
        title: The title of the blog post
        content: The main content of the blog post (HTML supported)
        parent_id: The ID of the parent blog (REQUIRED)
        summary: A short summary of the blog post (optional)
        allow_comments: Whether to allow comments on the post (default: True)
    
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
        # - Remove any non-alphanumeric characters except hyphens
        # - Convert to lowercase
        # - Replace spaces and other characters with hyphens
        # - Remove consecutive hyphens
        # - Remove leading/trailing hyphens
        # - Limit to 100 characters
        url_name = title.lower()
        # First replace spaces with hyphens
        url_name = url_name.replace(" ", "-")
        # Then replace all non-alphanumeric and non-hyphen characters
        url_name = re.sub(r'[^a-z0-9-]', '', url_name)
        # Replace multiple consecutive hyphens with a single one
        url_name = re.sub(r'-+', '-', url_name)
        # Remove leading/trailing hyphens
        url_name = url_name.strip('-')
        # Limit to 100 characters
        url_name = url_name[:100]
        
        post_data["UrlName"] = url_name
        
        logger.debug(f"Generated URL name: {url_name}")
        
        # Send POST request to create the blog post
        response = await make_post_request(ENDPOINTS["blog_posts"], post_data)
        
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
        data = await make_request(ENDPOINTS["blogs"])
        blogs = {blog["Id"]: blog["Title"] for blog in data.get("value", [])}
        logger.info(f"Found {len(blogs)} parent blogs")
        return blogs
    except Exception as e:
        logger.error(f"Error retrieving parent blogs: {str(e)}")
        return {} 