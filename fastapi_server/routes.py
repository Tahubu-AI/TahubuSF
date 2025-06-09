"""
API routes for the FastAPI server
"""
import logging
import json
from typing import Dict, Any, List, Union
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import tool functions
from tahubu_sf.api.news import get_news
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
    "createNewsItemDraft": create_news_item,  # Assuming create_news_item is defined
    "createListItemDraft": create_list_item,
    "createEventDraft": create_event,
    "createImageDraft": create_image,
    "createDocumentDraft": create_document,
    "createVideoDraft": create_video,
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
    eventstart: datetime
    eventend: datetime
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
    summary: str = None

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

@router.post("/blog-posts/draft", response_model=ContentResponse)
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
        return ContentResponse(
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

@router.post("/list-items/draft", response_model=ContentResponse)
async def create_list_item_draft(request: ListItemDraftRequest):
    """Create a new list item draft"""
    try:
        logger.info(f"Creating list item draft: {request.title}")
        
        # Validate required fields
        if not request.parent_id:
            raise HTTPException(
                status_code=400,
                detail="Parent list ID (parent_id) is required"
            )
        
        result = await create_list_item(
            title=request.title,
            content=request.content,
            parent_id=request.parent_id
        )
        
        # Extract ID and other info from result
        return ContentResponse(
            id=result.get("Id", "unknown"),
            title=request.title,
            url_name=result.get("UrlName", ""),
            status="draft"
        )
    except Exception as e:
        logger.exception(f"Error creating list item draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating list item draft: {str(e)}"
        )

@router.post("/events/draft", response_model=ContentResponse)
async def create_event_draft(request: EventDraftRequest):
    """Create a new event draft"""
    try:
        logger.info(f"Creating event draft: {request.title}")
        
        # Validate required fields
        if not request.parent_id:
            raise HTTPException(
                status_code=400,
                detail="Parent calendar ID (parent_id) is required"
            )
        
        result = await create_event(
            title=request.title,
            content=request.content,
            summary=request.summary,
            eventstart=request.eventstart,
            eventend=request.eventend,
            parent_id=request.parent_id
        )
        
        # Extract ID and other info from result
        return ContentResponse(
            id=result.get("Id", "unknown"),
            title=request.title,
            url_name=result.get("UrlName", ""),
            status="draft"
        )
    except Exception as e:
        logger.exception(f"Error creating event draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating event draft: {str(e)}"
        )

@router.post("/images/draft", response_model=ContentResponse)
async def create_image_draft(request: ImageDraftRequest):
    """Create a new image draft"""
    try:
        logger.info(f"Creating image draft: {request.title}")
        
        # Validate required fields
        if not request.parent_id:
            raise HTTPException(
                status_code=400,
                detail="Parent album ID (parent_id) is required"
            )
        
        result = await create_image(
            title=request.title,
            dalle_prompt=request.dalle_prompt,
            parent_id=request.parent_id
        )
        
        # Extract ID and other info from result
        return ContentResponse(
            id=result.get("Id", "unknown"),
            title=request.title,
            url_name=result.get("UrlName", ""),
            status="draft"
        )
    except Exception as e:
        logger.exception(f"Error creating image draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating image draft: {str(e)}"
        )

@router.post("/documents/draft", response_model=ContentResponse)
async def create_document_draft(request: DocumentDraftRequest):
    """Create a new document draft"""
    try:
        logger.info(f"Creating document draft: {request.title}")
        
        # Validate required fields
        if not request.parent_id:
            raise HTTPException(
                status_code=400,
                detail="Parent document library ID (parent_id) is required"
            )
        
        result = await create_document(
            title=request.title,
            content=request.content,
            summary=request.summary,
            parent_id=request.parent_id
        )
        
        # Extract ID and other info from result
        return ContentResponse(
            id=result.get("Id", "unknown"),
            title=request.title,
            url_name=result.get("UrlName", ""),
            status="draft"
        )
    except Exception as e:
        logger.exception(f"Error creating document draft: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating document draft: {str(e)}"
        )

@router.post("/videos/draft", response_model=ContentResponse)
async def create_video_draft(request: VideoDraftRequest):
    """Create a new video draft"""
    try:
        logger.info(f"Creating video draft: {request.title}")
        
        # Validate required fields
        if not request.parent_id:
            raise HTTPException(
                status_code=400,
                detail="Parent video library ID (parent_id) is required"
            )
        
        result = await create_video(
            title=request.title,
            content=request.content,
            parent_id=request.parent_id
        )
        
        # Extract ID and other info from result
        return ContentResponse(
            id=result.get("Id", "unknown"),
            title=request.title,
            url_name=result.get("UrlName", ""),
            status="draft"
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
    """List all available tools"""
    tools = []
    
    for name, func in TOOL_MAP.items():
        tools.append(ToolInfo(
            name=name,
            description=func.__doc__.strip() if func.__doc__ else "No description available"
        ))
        
    return ToolListResponse(tools=tools) 