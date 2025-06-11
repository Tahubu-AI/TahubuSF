#!/usr/bin/env python3
"""
FastMCP 2.0 HTTP Streaming Client
Demonstrates client capabilities including HTTP transport, authentication, and streaming
"""
import asyncio
import logging
import argparse
from typing import Dict, Any, Optional
import json

# Import the actual FastMCP client
try:
    from fastmcp import Client
    FASTMCP_AVAILABLE = True
except ImportError:
    # Fallback for basic HTTP client
    import httpx
    FASTMCP_AVAILABLE = False
    Client = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class TahubuSFClient:
    """
    FastMCP 2.0 HTTP Streaming Client for TahubuSF
    Provides high-level interface to the TahubuSF MCP server
    """
    
    def __init__(
        self, 
        server_url: str = "http://127.0.0.1:3000/mcp",
        auth_token: Optional[str] = None,
        use_streaming: bool = True
    ):
        self.server_url = server_url
        self.auth_token = auth_token
        self.use_streaming = use_streaming
        self.client = None
        
    async def connect(self):
        """Connect to the FastMCP 2.0 server"""
        logger.info(f"Connecting to FastMCP server at {self.server_url}")
        
        if FASTMCP_AVAILABLE:
            # Use FastMCP 2.0 native client
            self.client = Client(self.server_url)
            logger.info("Connected using FastMCP 2.0 native client")
        else:
            logger.error("FastMCP library not available - cannot connect")
            raise ImportError("FastMCP library required for client functionality")
    
    async def disconnect(self):
        """Disconnect from the server"""
        if self.client:
            # FastMCP client handles cleanup automatically
            logger.info("Disconnected from server")
    
    async def list_tools(self) -> list:
        """List available tools on the server"""
        logger.info("Listing available tools...")
        
        if not self.client:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        async with self.client:
            tools = await self.client.list_tools()
            logger.info(f"Found {len(tools)} tools")
            return tools
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Any:
        """Call a tool on the server"""
        if arguments is None:
            arguments = {}
            
        logger.info(f"Calling tool: {tool_name}")
        
        if not self.client:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        async with self.client:
            result = await self.client.call_tool(tool_name, arguments)
            logger.info(f"Tool {tool_name} completed successfully")
            return result
    
    async def get_news(self) -> str:
        """Get news items from Sitefinity"""
        return await self.call_tool("get_news")
    
    async def get_blog_posts(self) -> str:
        """Get blog posts from Sitefinity"""
        return await self.call_tool("get_blog_posts")
    
    async def create_blog_post(
        self, 
        title: str, 
        content: str, 
        parent_id: str,
        summary: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new blog post"""
        arguments = {
            "title": title,
            "content": content,
            "parent_id": parent_id
        }
        if summary:
            arguments["summary"] = summary
            
        return await self.call_tool("create_blog_post", arguments)

async def demo_client_usage():
    """Demonstrate FastMCP 2.0 client usage"""
    print("\n🚀 FastMCP 2.0 Client Demo")
    print("=" * 50)
    
    # Create and connect client
    client = TahubuSFClient(
        server_url="http://127.0.0.1:3000/mcp",
        use_streaming=True
    )
    
    try:
        await client.connect()
        
        # List available tools
        print("\n📋 Available Tools:")
        tools = await client.list_tools()
        for i, tool in enumerate(tools, 1):
            tool_name = tool.name if hasattr(tool, 'name') else str(tool)
            print(f"  {i}. {tool_name}")
        
        # Test some tools
        print("\n🧪 Testing Tools:")
        
        # Get news
        print("\n📰 Getting news...")
        try:
            news = await client.get_news()
            # Extract text content from MCP response
            if hasattr(news, '__iter__') and len(news) > 0:
                content = news[0].text if hasattr(news[0], 'text') else str(news[0])
            else:
                content = str(news)
            print(f"✅ News retrieved: {len(content)} characters")
        except Exception as e:
            print(f"❌ News failed: {e}")
        
        # Get blog posts
        print("\n📝 Getting blog posts...")
        try:
            blogs = await client.get_blog_posts()
            # Extract text content from MCP response
            if hasattr(blogs, '__iter__') and len(blogs) > 0:
                content = blogs[0].text if hasattr(blogs[0], 'text') else str(blogs[0])
            else:
                content = str(blogs)
            print(f"✅ Blog posts retrieved: {len(content)} characters")
        except Exception as e:
            print(f"❌ Blog posts failed: {e}")
        
        print("\n✅ FastMCP 2.0 client demo completed!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        logger.exception("Demo error")
    finally:
        await client.disconnect()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="TahubuSF FastMCP 2.0 Client Demo"
    )
    parser.add_argument(
        "--server-url",
        default="http://127.0.0.1:3000/mcp",
        help="FastMCP server URL (default: http://127.0.0.1:3000/mcp)"
    )
    parser.add_argument(
        "--auth-token",
        help="Authentication token"
    )
    parser.add_argument(
        "--no-streaming",
        action="store_true",
        help="Disable streaming responses"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run the demo
    asyncio.run(demo_client_usage())

if __name__ == "__main__":
    main() 