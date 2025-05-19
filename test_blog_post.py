"""
Test script to create a blog post draft using the TahubuSF API
"""
import asyncio
import logging
import sys
from dotenv import load_dotenv

from tahubu_sf.api.blog_posts import create_blog_post_draft, get_parent_blogs

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_blog_post")

# Load environment variables
load_dotenv()

async def test_create_blog_post():
    """Test creating a blog post draft"""
    # Get parent blogs
    logger.info("Getting available parent blogs...")
    parent_blogs = await get_parent_blogs()
    
    if parent_blogs:
        logger.info(f"Found {len(parent_blogs)} parent blogs")
        # Get first parent blog ID if available
        parent_id = next(iter(parent_blogs.keys()), None)
    else:
        logger.info("No parent blogs found")
        parent_id = None
    
    # Sample blog post content
    title = "Test Blog Post via API"
    content = """
    <h2>This is a test blog post created via the API</h2>
    <p>This post was created as a draft using the TahubuSF API.</p>
    <p>It demonstrates how to programmatically create blog posts in Sitefinity.</p>
    <ul>
        <li>Feature 1</li>
        <li>Feature 2</li>
        <li>Feature 3</li>
    </ul>
    """
    summary = "A test blog post created via the TahubuSF API"
    
    logger.info(f"Creating blog post draft with title: {title}")
    if parent_id:
        parent_name = parent_blogs.get(parent_id, "Unknown")
        logger.info(f"Using parent blog: {parent_name} (ID: {parent_id})")
    else:
        logger.info("No parent blog selected")
    
    # Create the blog post
    result = await create_blog_post_draft(
        title=title,
        content=content,
        summary=summary,
        parent_id=parent_id
    )
    
    logger.info(f"Blog post created successfully with ID: {result.get('Id', 'unknown')}")
    logger.info(f"URL name: {result.get('UrlName', 'unknown')}")
    return result

if __name__ == "__main__":
    logger.info("Starting blog post test...")
    try:
        result = asyncio.run(test_create_blog_post())
        logger.info("Test completed successfully.")
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        sys.exit(1) 