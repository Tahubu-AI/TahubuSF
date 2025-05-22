"""
API routes for the FastAPI server
"""
import logging
import json
from typing import Dict, Any, List, Union

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import tool functions
from tahubu_sf.api.news import get_news
from tahubu_sf.api.blogs import get_blog_posts
from tahubu_sf.api.blog_posts import create_blog_post, get_parent_blogs
from tahubu_sf.api.pages import get_pages, get_page_templates
from tahubu_sf.api.sites import get_sites

# Configure logging
logger = logging.getLogger("tahubu_sf.fastapi.routes")

# Create router
router = APIRouter(prefix="/api")

# Tool mapping for direct execution
TOOL_MAP = {
    "getNews": get_news,
    "getBlogPosts": get_blog_posts,
    "getPages": get_pages,
    "getPageTemplates": get_page_templates,
    "getSites": get_sites,
    "createBlogPostDraft": create_blog_post,
    "getParentBlogs": get_parent_blogs,
}

# Data models
class ToolRequest(BaseModel):
    """Request model for tool execution"""
    name: str
    params: Dict[str, Any] = {}

class ToolResponse(BaseModel):
    """Response model for tool execution"""
    result: Any = Field(description="Tool result that can be string, dict, or other JSON-serializable data")

class ToolInfo(BaseModel):
    """Information about a tool"""
    name: str
    description: str

class ToolListResponse(BaseModel):
    """Response model for tool listing"""
    tools: List[ToolInfo]

# Blog post specific models
class BlogPostDraftRequest(BaseModel):
    """Request model for creating a blog post draft"""
    title: str
    content: str
    summary: str = None
    parent_id: str
    allow_comments: bool = True

class BlogPostResponse(BaseModel):
    """Response model for a created blog post"""
    id: str
    title: str
    url_name: str
    status: str

@router.post("/run-tool")
async def run_tool(request: ToolRequest):
    """Execute a tool directly with provided parameters"""
    try:
        tool_name = request.name
        params = request.params
        
        logger.info(f"Running tool: {tool_name} with params: {params}")
        
        if tool_name not in TOOL_MAP:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown tool: {tool_name}"
            )
            
        # Run the tool function
        result = await TOOL_MAP[tool_name](**params)
        
        # Return a JSON response directly to handle any result type
        return {"result": result}
    except Exception as e:
        logger.exception(f"Error running tool: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error running tool: {str(e)}"
        )

@router.post("/blog-posts/draft", response_model=BlogPostResponse)
async def create_blog_draft(request: BlogPostDraftRequest):
    """Create a new blog post draft"""
    try:
        logger.info(f"Creating blog post draft: {request.title}")
        
        # Validate required fields
        if not request.parent_id:
            raise HTTPException(
                status_code=400,
                detail="Parent blog ID (parent_id) is required"
            )
        
        result = await create_blog_post(
            title=request.title,
            content=request.content,
            summary=request.summary,
            parent_id=request.parent_id,
            allow_comments=request.allow_comments
        )
        
        # Extract ID and other info from result
        return BlogPostResponse(
            id=result.get("Id", "unknown"),
            title=request.title,
            url_name=result.get("UrlName", ""),
            status="draft"
        )
    except Exception as e:
        logger.exception(f"Error creating blog post draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating blog post draft: {str(e)}"
        )

@router.get("/blog-parents", response_model=Dict[str, str])
async def get_blog_parents():
    """Get a list of available parent blogs"""
    try:
        return await get_parent_blogs()
    except Exception as e:
        logger.exception(f"Error getting parent blogs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting parent blogs: {str(e)}"
        )

@router.get("/list-tools", response_model=ToolListResponse)
async def list_tools():
    """List all available tools"""
    tools = []
    
    for name, func in TOOL_MAP.items():
        tools.append(ToolInfo(
            name=name,
            description=func.__doc__.strip() if func.__doc__ else "No description available"
        ))
        
    return ToolListResponse(tools=tools) 