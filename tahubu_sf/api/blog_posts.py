"""
API endpoints for creating and managing blog posts
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional, List

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

async def get_blog_post_by_id(post_id: str) -> Dict[str, Any]:
    """
    Get a single blog post by its ID.
    
    Args:
        post_id: The ID of the blog post to retrieve
        
    Returns:
        Dict[str, Any]: The complete blog post data
    """
    try:
        endpoint = f"{POSTS_CONTENT_ENDPOINT}({post_id})"
        data = await make_request(endpoint)
        return data
    except Exception as e:
        logger.error(f"Error retrieving blog post {post_id}: {str(e)}")
        raise Exception(f"Failed to retrieve blog post: {str(e)}") from e

async def get_blog_posts() -> Dict[str, Any]:
    """
    Get blog posts from the Sitefinity site with pagination support.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - total_count: Total number of blog posts
            - posts: List of blog posts with limited properties
            - has_more: Boolean indicating if there are more posts
    """
    try:
        # Get posts with count included in the response
        data = await make_request(
            POSTS_CONTENT_ENDPOINT,
            params={
                "$count": "true",
                "$select": "Id,PublicationDate,Title,ItemDefaultUrl,AllowComments,Summary,ParentId,Content"
            }
        )
        
        # Process posts to handle summary/content
        posts = []
        for post in data.get("value", []):
            # Get summary or first 100 chars of content
            summary = post.get("Summary", "")
            if not summary and "Content" in post:
                content = post.get("Content", "")
                # Remove HTML tags for summary
                content = re.sub(r'<[^>]+>', '', content)
                summary = content[:100] + "..." if len(content) > 100 else content
            
            # Create post with limited properties
            processed_post = {
                "Id": post.get("Id"),
                "PublicationDate": post.get("PublicationDate"),
                "Title": post.get("Title"),
                "ItemDefaultUrl": post.get("ItemDefaultUrl"),
                "AllowComments": post.get("AllowComments"),
                "Summary": summary,
                "ParentId": post.get("ParentId")
            }
            posts.append(processed_post)
        
        return {
            "total_count": data.get("@odata.count", 0),
            "posts": posts,
            "has_more": "@odata.nextLink" in data
        }
        
    except Exception as e:
        logger.error(f"Error retrieving blog posts: {str(e)}")
        raise Exception(f"Failed to retrieve blog posts: {str(e)}") from e 