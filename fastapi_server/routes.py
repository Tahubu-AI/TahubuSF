"""
API routes for the FastAPI server
"""
import logging
from typing import Dict, Any, List

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import tool functions
from tahubu_sf.api.news import get_news
from tahubu_sf.api.blogs import get_blog_posts
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
}

# Data models
class ToolRequest(BaseModel):
    """Request model for tool execution"""
    name: str
    params: Dict[str, Any] = {}

class ToolResponse(BaseModel):
    """Response model for tool execution"""
    result: str

class ToolInfo(BaseModel):
    """Information about a tool"""
    name: str
    description: str

class ToolListResponse(BaseModel):
    """Response model for tool listing"""
    tools: List[ToolInfo]

@router.post("/run-tool", response_model=ToolResponse)
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
        
        return ToolResponse(result=result)
    except Exception as e:
        logger.exception(f"Error running tool: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error running tool: {str(e)}"
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