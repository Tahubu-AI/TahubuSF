#!/usr/bin/env python
"""
Simple HTTP JSON API server to run MCP tools directly using the modular code structure
"""
import json
import asyncio
import webbrowser
import os
import sys
import mimetypes
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add the project root to the path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from our modular architecture
from tahubu_sf.api.news import get_news
from tahubu_sf.api.blogs import get_blog_posts
from tahubu_sf.api.pages import get_pages, get_page_templates
from tahubu_sf.api.sites import get_sites
from tahubu_sf.config.settings import AUTH_TYPE, API_KEY, USERNAME

# Initialize mime types and logging
mimetypes.init()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("tahubu_sf.simple_server")

class MCPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests - serve HTML UI and static files"""
        if self.path == "/" or self.path == "":
            # Serve the main HTML page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("inspector.html", "r") as f:
                self.wfile.write(f.read().encode())
        elif self.path.startswith("/media/"):
            # Serve files from the media directory
            try:
                file_path = self.path[1:]  # Remove leading '/'
                with open(file_path, "rb") as f:
                    # Determine content type
                    content_type, _ = mimetypes.guess_type(file_path)
                    if content_type is None:
                        content_type = "application/octet-stream"
                    
                    self.send_response(200)
                    self.send_header("Content-type", content_type)
                    self.end_headers()
                    self.wfile.write(f.read())
            except (FileNotFoundError, IOError):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
        else:
            # Handle all other paths
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            
    def do_POST(self):
        """Handle POST requests to execute MCP tools"""
        if self.path == "/api/run-tool":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            request = json.loads(post_data)
            
            tool_name = request.get("name")
            params = request.get("params", {})
            
            logger.info(f"Running tool: {tool_name} with params: {params}")
            
            try:
                result = self.execute_tool(tool_name, params)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                response = {"result": result}
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}", exc_info=True)
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def execute_tool(self, tool_name, params):
        """Execute the specified tool with parameters"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Use the modular code structure
            if tool_name == "getNews":
                result = loop.run_until_complete(get_news())
            elif tool_name == "getBlogPosts":
                result = loop.run_until_complete(get_blog_posts())
            elif tool_name == "getPages":
                result = loop.run_until_complete(get_pages())
            elif tool_name == "getPageTemplates":
                result = loop.run_until_complete(get_page_templates())
            elif tool_name == "getSites":
                result = loop.run_until_complete(get_sites())
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
                
            return result
        finally:
            loop.close()

def run_server(port=None, host=None):
    """Run the HTTP server"""
    # Get port from environment variable or use default
    port = port or int(os.getenv("PORT", 7777))
    host = host or os.getenv("HOST", "localhost")
    
    server = HTTPServer((host, port), MCPRequestHandler)
    logger.info(f"Server started at http://{host}:{port}")
    logger.info(f"Retry configuration: MAX_ATTEMPTS={os.getenv('RETRY_MAX_ATTEMPTS', '3')}, "
               f"MIN_WAIT={os.getenv('RETRY_MIN_SECONDS', '1')}s, "
               f"MAX_WAIT={os.getenv('RETRY_MAX_SECONDS', '10')}s")
    logger.info(f"Sitefinity configuration: SITE_PREFIX={os.getenv('SITEFINITY_SITE_PREFIX', '')}")
    
    # Log authentication configuration
    auth_info = f"Authentication type: {AUTH_TYPE}"
    if AUTH_TYPE == "apikey":
        auth_info += f", API Key: {'configured' if API_KEY else 'not configured'}"
    elif AUTH_TYPE in ["authenticated", "administrator"]:
        auth_info += f", Username: {'configured' if USERNAME else 'not configured'}"
    logger.info(auth_info)
    
    logger.info("Open your browser to this URL to test MCP tools")
    
    # Open browser automatically
    webbrowser.open(f"http://{host}:{port}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        logger.info("Server stopped")

if __name__ == "__main__":
    run_server() 