"""
Debugging script for Sitefinity API requests and responses
"""
import asyncio
import logging
import sys
import json
import httpx
from dotenv import load_dotenv

from tahubu_sf.config.settings import ENDPOINTS, AUTH_TYPE, API_KEY, AUTH_KEY
from tahubu_sf.utils.http import get_auth_token

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("debug_sitefinity")

# Load environment variables
load_dotenv()

async def inspect_api_response(url, method="GET", params=None):
    """
    Make a request to the Sitefinity API and inspect the response format
    
    Args:
        url: The URL to request
        method: HTTP method (GET, OPTIONS, etc.)
        params: Optional query parameters
    """
    logger.info(f"Inspecting {method} {url}")
    
    # Get authentication headers
    auth_headers = await get_auth_token()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;odata.metadata=minimal",
        **auth_headers
    }
    
    logger.info(f"Authentication type: {AUTH_TYPE}")
    logger.info(f"Headers: {json.dumps(headers)}")
    
    if params:
        logger.info(f"Parameters: {json.dumps(params)}")
    
    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=headers, params=params)
            else:
                # For OPTIONS method to check what's allowed
                response = await client.options(url, headers=headers)
                
            # Print response details
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {json.dumps(dict(response.headers))}")
            
            # Try to parse as JSON
            try:
                data = response.json()
                logger.info(f"Response body: {json.dumps(data, indent=2)}")
                return data
            except:
                logger.info(f"Response body (text): {response.text}")
                return response.text
    except Exception as e:
        logger.error(f"Error inspecting API: {str(e)}")
        return None

async def inspect_blog_post_example():
    """Check a blog post example to understand its format"""
    # First get list of blog posts to see their format
    posts_url = ENDPOINTS["blog_posts"]
    logger.info(f"Getting blog posts from {posts_url}")
    
    # Add OData parameters
    odata_params = {
        "$top": "5",  # Limit to 5 results
        "$orderby": "PublicationDate desc",
        "$format": "json",
        "$select": "Id,Title,PublicationDate,UrlName,ParentId"  # Select specific fields
    }
    
    # Try to get a list of posts
    posts = await inspect_api_response(posts_url, params=odata_params)
    
    # If we got posts, check the first one to see its format
    if posts and isinstance(posts, dict) and "value" in posts and posts["value"]:
        first_post = posts["value"][0]
        post_id = first_post.get("Id")
        
        if post_id:
            # Get the individual post to see full details
            # Format the URL correctly for OData
            post_url = f"{posts_url}({post_id})"
            logger.info(f"Getting detailed post from {post_url}")
            post_details = await inspect_api_response(post_url)
            
            # Extract important fields for creating a post
            if post_details:
                logger.info("Important fields for blog post creation:")
                important_fields = [
                    "Title", "Content", "Summary", "PublicationDate", 
                    "UrlName", "ParentId", "AllowComments", "Status"
                ]
                
                for field in important_fields:
                    if field in post_details:
                        logger.info(f"  {field}: {post_details.get(field)}")
                    else:
                        logger.info(f"  {field}: <not present>")
    
    # Check options on the blog posts endpoint
    logger.info("Checking OPTIONS for blog posts endpoint")
    await inspect_api_response(posts_url, method="OPTIONS")
    
    # Also check blogs (not blog posts) endpoint
    blogs_url = ENDPOINTS["blogs"]
    logger.info(f"Getting blogs from {blogs_url}")
    blogs = await inspect_api_response(blogs_url, params={
        "$top": "10",
        "$select": "Id,Title",
        "$format": "json"
    })
    
    if blogs and isinstance(blogs, dict) and "value" in blogs and blogs["value"]:
        logger.info(f"Found {len(blogs['value'])} blogs")
        for blog in blogs["value"]:
            logger.info(f"Blog: {blog.get('Title')} (ID: {blog.get('Id')})")

async def debug_create_blog_post():
    """Debug creating a blog post by examining the JSON data structure"""
    # Example blog post data
    post_data = {
        "Title": "Debug Test Blog Post",
        "Content": "<p>This is a test blog post for debugging.</p>",
        "Summary": "A debugging test post",
        "UrlName": "debug-test-blog-post",
        "PublicationDate": "2025-05-19T23:45:00Z",
        "AllowComments": True,
        "IncludeInSitemap": True
    }
    
    # Get blogs to find a parent ID
    blogs_url = ENDPOINTS["blogs"]
    blogs = await inspect_api_response(blogs_url)
    
    if blogs and isinstance(blogs, dict) and "value" in blogs and blogs["value"] and blogs["value"]:
        # Get the first blog as parent
        first_blog = blogs["value"][0]
        post_data["ParentId"] = first_blog.get("Id")
        logger.info(f"Using parent blog: {first_blog.get('Title')} (ID: {first_blog.get('Id')})")
    
    # Print the data that would be sent
    logger.info(f"Blog post creation data that would be sent: {json.dumps(post_data, indent=2)}")

if __name__ == "__main__":
    logger.info("Starting Sitefinity API debug...")
    asyncio.run(inspect_blog_post_example())
    logger.info("Running blog post creation debug...")
    asyncio.run(debug_create_blog_post())
    logger.info("Debug completed.") 