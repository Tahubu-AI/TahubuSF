"""
API routes for the FastAPI server
"""
import logging
import json
from typing import Dict, Any, List, Union, Optional
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import tool functions
from tahubu_sf.api.news import get_news, create_news_item  # Assuming create_news_item is defined
from tahubu_sf.api.blogs import get_blog_posts
from tahubu_sf.api.blog_posts import create_blog_post, get_parent_blogs
from tahubu_sf.api.lists import get_list_items
from tahubu_sf.api.list_items import create_list_item, get_parent_lists
from tahubu_sf.api.calendars import get_events
from tahubu_sf.api.events import get_calendars, create_event
from tahubu_sf.api.pages import get_pages, get_page_templates
from tahubu_sf.api.sites import get_sites
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
logger = logging.getLogger("tahubu_sf.fastapi.routes")

# Create router
router = APIRouter(prefix="/api")

# Tool mapping for direct execution
TOOL_MAP = {
    "getNews": get_news,
    "getBlogPosts": get_blog_posts,
    "getListItems": get_list_items,
    "getEvents": get_events,
    "getForms": get_forms,
    "getCalendars": get_calendars,
    "getSharedContent": get_shared_content,
    "getPages": get_pages,
    "getPageTemplates": get_page_templates,
    "getSites": get_sites,
    "getParentBlogs": get_parent_blogs,
    "getParentLists": get_parent_lists,
    "getAlbums": get_albums,
    "getImages": get_images,
    "getDocumentLibraries": get_document_libraries,
    "getDocuments": get_documents,
    "getVideos": get_videos,
    "getVideoLibraries": get_video_libraries,
    "getSearchIndexes": get_search_indexes,
    "getTaxonomies": get_taxonomies,
    "getSectionPresets": get_section_presets,
    "createBlogPostDraft": create_blog_post,
    "createNewsItemDraft": create_news_item,
    "createListItemDraft": create_list_item,
    "createEventDraft": create_event,
    "createImageDraft": create_image,
    "createDocumentDraft": create_document,
    "createVideoDraft": create_video,
    "createListItemDraft": create_list_item,
    "createEventDraft": create_event,
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
    schema: Dict[str, Any] = {}  # Parameter schema information

class ToolListResponse(BaseModel):
    """Response model for tool listing"""
    tools: List[ToolInfo]

# Define tool schemas for better discoverability
TOOL_SCHEMAS = {
    "createBlogPostDraft": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the blog post"},
            "content": {"type": "string", "description": "The main content of the blog post (HTML supported)"},
            "summary": {"type": "string", "description": "A short summary of the blog post"},
            "parent_id": {"type": "string", "description": "The ID of the parent blog (use getParentBlogs to find)"},
            "allow_comments": {"type": "boolean", "description": "Whether to allow comments", "default": True}
        },
        "required": ["title", "content", "parent_id"]
    },
    "createListItemDraft": {
        "type": "object", 
        "properties": {
            "title": {"type": "string", "description": "The title of the list item"},
            "content": {"type": "string", "description": "The main content of the list item"},
            "parent_id": {"type": "string", "description": "The ID of the parent list (use getParentLists to find)"}
        },
        "required": ["title", "content", "parent_id"]
    },
    "createEventDraft": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the event"},
            "content": {"type": "string", "description": "The description of the event"},
            "summary": {"type": "string", "description": "A short summary of the event"},
            "eventstart": {"type": "string", "format": "date-time", "description": "Event start date/time (ISO format)"},
            "eventend": {"type": "string", "format": "date-time", "description": "Event end date/time (ISO format)"},
            "parent_id": {"type": "string", "description": "The ID of the parent calendar (use getCalendars to find)"}
        },
        "required": ["title", "content", "parent_id"]
    },
    "createNewsItemDraft": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the news item"},
            "content": {"type": "string", "description": "The main content of the news item (HTML supported)"},
            "summary": {"type": "string", "description": "A short summary of the news item"},
            "allow_comments": {"type": "boolean", "description": "Whether to allow comments", "default": True}
        },
        "required": ["title", "content"]
    },
    "createImageDraft": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the image"},
            "dalle_prompt": {"type": "string", "description": "DALL-E prompt for generating the image"},
            "parent_id": {"type": "string", "description": "The ID of the parent album (use getAlbums to find)"}
        },
        "required": ["title", "dalle_prompt", "parent_id"]
    },
    "createDocumentDraft": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the document"},
            "content": {"type": "string", "description": "The content of the document"},
            "summary": {"type": "string", "description": "A short summary of the document"},
            "parent_id": {"type": "string", "description": "The ID of the parent document library (use getDocumentLibraries to find)"}
        },
        "required": ["title", "content", "parent_id"]
    },
    "createVideoDraft": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the video"},
            "content": {"type": "string", "description": "The description of the video"},
            "parent_id": {"type": "string", "description": "The ID of the parent video library (use getVideoLibraries to find)"}
        },
        "required": ["title", "content", "parent_id"]
    }
}

# Blog post specific models
class BlogPostDraftRequest(BaseModel):
    """Request model for creating a blog post draft"""
    title: str
    content: str
    summary: Optional[str] = None
    parent_id: str
    allow_comments: bool = True

class ListItemDraftRequest(BaseModel):
    """Request model for creating a list item draft"""
    title: str
    content: str
    parent_id: str

class EventDraftRequest(BaseModel):
    """Request model for creating an event draft"""
    title: str
    content: str
    summary: str
    eventstart: Optional[datetime] = None
    eventend: Optional[datetime] = None
    parent_id: str

class ImageDraftRequest(BaseModel):
    """Request model for creating an image draft"""
    title: str
    dalle_prompt: str
    parent_id: str

class DocumentDraftRequest(BaseModel):
    """Request model for creating a document draft"""
    title: str
    content: str
    parent_id: str
    summary: Optional[str] = None

class VideoDraftRequest(BaseModel):
    """Request model for creating a video draft"""
    title: str
    content: str
    parent_id: str

class ContentResponse(BaseModel):
    """Response model for created content"""
    id: str
    title: str
    url_name: str
    status: str

async def _execute_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Internal function that executes any tool with given parameters.
    This is the single source of truth for tool execution logic.
    """
    logger.info(f"Executing tool: {tool_name} with params: {params}")
    
    if tool_name not in TOOL_MAP:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown tool: {tool_name}"
        )
        
    # For creation tools, call the underlying API functions directly
    if tool_name == "createBlogPostDraft":
        # Extract required parameters
        title = params.get("title")
        content = params.get("content")
        summary = params.get("summary")
        parent_id = params.get("parent_id")
        allow_comments = params.get("allow_comments", True)
        
        # Validate required parameters
        if not title or not content or not parent_id:
            missing = []
            if not title:
                missing.append("title")
            if not content:
                missing.append("content")
            if not parent_id:
                missing.append("parent_id")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameters: {', '.join(missing)}"
            )
        
        # Call the underlying API function directly
        result = await create_blog_post(
            title=title,
            content=content,
            summary=summary,
            parent_id=parent_id,
            allow_comments=allow_comments
        )
        
        return result
    
    elif tool_name == "createListItemDraft":
        # Extract required parameters
        title = params.get("title")
        content = params.get("content")
        parent_id = params.get("parent_id")
        
        # Validate required parameters
        if not title or not content or not parent_id:
            missing = []
            if not title:
                missing.append("title")
            if not content:
                missing.append("content")
            if not parent_id:
                missing.append("parent_id")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameters: {', '.join(missing)}"
            )
        
        # Call the underlying API function directly
        result = await create_list_item(
            title=title,
            content=content,
            parent_id=parent_id,
        )
        
        return result
    
    elif tool_name == "createEventDraft":
        # Extract required parameters
        title = params.get("title")
        content = params.get("content")
        summary = params.get("summary")
        parent_id = params.get("parent_id")
        event_start = params.get("eventstart")
        event_end = params.get("eventend")
        
        # Validate required parameters
        if not title or not content or not parent_id:
            missing = []
            if not title:
                missing.append("title")
            if not content:
                missing.append("content")
            if not parent_id:
                missing.append("parent_id")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameters: {', '.join(missing)}"
            )
        
        # Call the underlying API function directly
        result = await create_event(
            title=title,
            content=content,
            summary=summary,
            parent_id=parent_id,
            eventstart=event_start,
            eventend=event_end
        )
        
        return result
    
    elif tool_name == "createNewsItemDraft":
        # Extract required parameters
        title = params.get("title")
        content = params.get("content")
        summary = params.get("summary")
        allow_comments = params.get("allow_comments", True)
        
        # Validate required parameters
        if not title or not content:
            missing = []
            if not title:
                missing.append("title")
            if not content:
                missing.append("content")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameters: {', '.join(missing)}"
            )
        
        # Call the underlying API function directly
        result = await create_news_item(
            title=title,
            content=content,
            summary=summary,
            allow_comments=allow_comments
        )
        
        return result
    
    elif tool_name == "createImageDraft":
        # Extract required parameters
        title = params.get("title")
        dalle_prompt = params.get("dalle_prompt")
        parent_id = params.get("parent_id")
        
        # Validate required parameters
        if not title or not dalle_prompt or not parent_id:
            missing = []
            if not title:
                missing.append("title")
            if not dalle_prompt:
                missing.append("dalle_prompt")
            if not parent_id:
                missing.append("parent_id")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameters: {', '.join(missing)}"
            )
        
        # Call the underlying API function directly
        result = await create_image(
            title=title,
            dalle_prompt=dalle_prompt,
            parent_id=parent_id
        )
        
        return result
    
    elif tool_name == "createDocumentDraft":
        # Extract required parameters
        title = params.get("title")
        content = params.get("content")
        parent_id = params.get("parent_id")
        summary = params.get("summary")
        
        # Validate required parameters
        if not title or not content or not parent_id:
            missing = []
            if not title:
                missing.append("title")
            if not content:
                missing.append("content")
            if not parent_id:
                missing.append("parent_id")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameters: {', '.join(missing)}"
            )
        
        # Call the underlying API function directly
        result = await create_document(
            title=title,
            content=content,
            summary=summary,
            parent_id=parent_id
        )
        
        return result
    
    elif tool_name == "createVideoDraft":
        # Extract required parameters
        title = params.get("title")
        content = params.get("content")
        parent_id = params.get("parent_id")
        
        # Validate required parameters
        if not title or not content or not parent_id:
            missing = []
            if not title:
                missing.append("title")
            if not content:
                missing.append("content")
            if not parent_id:
                missing.append("parent_id")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameters: {', '.join(missing)}"
            )
        
        # Call the underlying API function directly
        result = await create_video(
            title=title,
            content=content,
            parent_id=parent_id
        )
        
        return result
    
    else:
        # For read-only tools, run the function directly (these work fine)
        result = await TOOL_MAP[tool_name](**params)
        return result

@router.post("/run-tool")
async def run_tool(request: ToolRequest):
    """
    Execute any MCP tool directly with provided parameters.
    
    This is the MCP-compatible unified endpoint that handles all 28 tools.
    Use this endpoint for:
    - MCP client integration
    - Multi-tool automation
    - Consistent tool execution pattern
    
    For traditional REST API usage, use the specific endpoints instead:
    - POST /api/blog-posts/draft for blog posts
    - POST /api/events/draft for events  
    - etc.
    """
    try:
        result = await _execute_tool(request.name, request.params)
        return {"result": result}
        
    except HTTPException:
        # Re-raise HTTP exceptions (they have proper status codes)
        raise
    except Exception as e:
        logger.exception(f"Error running tool: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error running tool: {str(e)}"
        )

@router.post("/blog-posts/draft", response_model=ContentResponse)
async def create_blog_draft(request: BlogPostDraftRequest):
    """
    Create a new blog post draft (REST endpoint).
    
    This is a traditional REST API endpoint with Pydantic validation.
    For MCP clients, use POST /api/run-tool with tool name 'createBlogPostDraft' instead.
    """
    try:
        logger.info(f"Creating blog post draft: {request.title}")
        
        # Convert Pydantic model to params dict and delegate to shared execution logic
        params = {
            "title": request.title,
            "content": request.content,
            "summary": request.summary,
            "parent_id": request.parent_id,
            "allow_comments": request.allow_comments
        }
        
        result = await _execute_tool("createBlogPostDraft", params)
        
        # Return in ContentResponse format
        return ContentResponse(
            id=result["id"],
            title=result["title"],
            url_name=result["url_name"],
            status=result["status"]
        )
    except Exception as e:
        logger.exception(f"Error creating blog post draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating blog post draft: {str(e)}"
        )

@router.post("/list-items/draft", response_model=ContentResponse)
async def create_list_item_draft(request: ListItemDraftRequest):
    """Create a new list item draft (REST endpoint)"""
    try:
        logger.info(f"Creating list item draft: {request.title}")
        
        # Convert Pydantic model to params dict and delegate to shared execution logic
        params = {
            "title": request.title,
            "content": request.content,
            "parent_id": request.parent_id
        }
        
        result = await _execute_tool("createListItemDraft", params)
        
        # Return in ContentResponse format
        return ContentResponse(
            id=result["id"],
            title=result["title"],
            url_name=result["url_name"],
            status=result["status"]
        )
    except Exception as e:
        logger.exception(f"Error creating list item draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating list item draft: {str(e)}"
        )

@router.post("/events/draft", response_model=ContentResponse)
async def create_event_draft(request: EventDraftRequest):
    """Create a new event draft (REST endpoint)"""
    try:
        logger.info(f"Creating event draft: {request.title}")
        
        # Convert Pydantic model to params dict and delegate to shared execution logic
        params = {
            "title": request.title,
            "content": request.content,
            "summary": request.summary,
            "parent_id": request.parent_id,
            "eventstart": request.eventstart,
            "eventend": request.eventend
        }
        
        result = await _execute_tool("createEventDraft", params)
        
        # Return in ContentResponse format
        return ContentResponse(
            id=result["id"],
            title=result["title"],
            url_name=result["url_name"],
            status=result["status"]
        )
    except Exception as e:
        logger.exception(f"Error creating event draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating event draft: {str(e)}"
        )

@router.post("/images/draft", response_model=ContentResponse)
async def create_image_draft(request: ImageDraftRequest):
    """Create a new image draft (REST endpoint)"""
    try:
        logger.info(f"Creating image draft: {request.title}")
        
        # Convert Pydantic model to params dict and delegate to shared execution logic
        params = {
            "title": request.title,
            "dalle_prompt": request.dalle_prompt,
            "parent_id": request.parent_id
        }
        
        result = await _execute_tool("createImageDraft", params)
        
        # Return in ContentResponse format
        return ContentResponse(
            id=result["id"],
            title=result["title"],
            url_name=result["url_name"],
            status=result["status"]
        )
    except Exception as e:
        logger.exception(f"Error creating image draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating image draft: {str(e)}"
        )

@router.post("/documents/draft", response_model=ContentResponse)
async def create_document_draft(request: DocumentDraftRequest):
    """Create a new document draft (REST endpoint)"""
    try:
        logger.info(f"Creating document draft: {request.title}")
        
        # Convert Pydantic model to params dict and delegate to shared execution logic
        params = {
            "title": request.title,
            "content": request.content,
            "parent_id": request.parent_id,
            "summary": request.summary
        }
        
        result = await _execute_tool("createDocumentDraft", params)
        
        # Return in ContentResponse format
        return ContentResponse(
            id=result["id"],
            title=result["title"],
            url_name=result["url_name"],
            status=result["status"]
        )
    except Exception as e:
        logger.exception(f"Error creating document draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating document draft: {str(e)}"
        )

@router.post("/videos/draft", response_model=ContentResponse)
async def create_video_draft(request: VideoDraftRequest):
    """Create a new video draft (REST endpoint)"""
    try:
        logger.info(f"Creating video draft: {request.title}")
        
        # Convert Pydantic model to params dict and delegate to shared execution logic
        params = {
            "title": request.title,
            "content": request.content,
            "parent_id": request.parent_id
        }
        
        result = await _execute_tool("createVideoDraft", params)
        
        # Return in ContentResponse format
        return ContentResponse(
            id=result["id"],
            title=result["title"],
            url_name=result["url_name"],
            status=result["status"]
        )
    except Exception as e:
        logger.exception(f"Error creating video draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating video draft: {str(e)}"
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

@router.get("/list-parents", response_model=Dict[str, str])
async def get_list_parents():
    """Get a list of available parent lists"""
    try:
        return await get_parent_lists()
    except Exception as e:
        logger.exception(f"Error getting parent lists: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting parent lists: {str(e)}"
        )

@router.get("/calendars", response_model=Dict[str, str])
async def get_calendar_list():
    """Get a list of available calendars"""
    try:
        return await get_calendars()
    except Exception as e:
        logger.exception(f"Error getting calendars: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting calendars: {str(e)}"
        )

@router.get("/albums", response_model=Dict[str, str])
async def get_album_list():
    """Get a list of available albums"""
    try:
        return await get_albums()
    except Exception as e:
        logger.exception(f"Error getting albums: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting albums: {str(e)}"
        )

@router.get("/document-libraries", response_model=Dict[str, str])
async def get_document_library_list():
    """Get a list of available document libraries"""
    try:
        return await get_document_libraries()
    except Exception as e:
        logger.exception(f"Error getting document libraries: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting document libraries: {str(e)}"
        )

@router.get("/video-libraries", response_model=Dict[str, str])
async def get_video_library_list():
    """Get a list of available video libraries"""
    try:
        return await get_video_libraries()
    except Exception as e:
        logger.exception(f"Error getting video libraries: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting video libraries: {str(e)}"
        )

@router.get("/list-tools", response_model=ToolListResponse)
async def list_tools():
    """List all available tools with descriptions and parameter schemas"""
    tools = []
    
    for name, func in TOOL_MAP.items():
        # Get tool description from docstring
        description = func.__doc__.strip() if func.__doc__ else "No description available"
        
        # Get parameter schema if available
        schema = TOOL_SCHEMAS.get(name, {})
        
        tools.append(ToolInfo(
            name=name,
            description=description,
            schema=schema
        ))
        
    return ToolListResponse(tools=tools) 