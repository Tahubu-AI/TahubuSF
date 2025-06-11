# TahubuSF FastMCP 2.0 Implementation

🚀 **Advanced HTTP Streaming Transport Protocol with Authentication & Proxying**

This folder contains the FastMCP 2.0 implementation that adds advanced capabilities to your existing TahubuSF MCP tools, including HTTP streaming transport, authentication, remote server proxying, and client support.

## 🆕 What's New with FastMCP 2.0

FastMCP 2.0 provides comprehensive features that go far beyond the core MCP specification:

### 🌐 **HTTP Streaming Transport**

- Real-time streaming responses via MCP protocol
- Server-Sent Events (SSE) support
- Streamable HTTP transport
- Efficient connection management

### 🔐 **Authentication & Security**

- Bearer token authentication
- API key authentication
- JWT token support
- Configurable CORS policies
- Rate limiting

### 🔄 **Remote Server Proxying**

- Proxy multiple MCP servers
- Load balancing capabilities
- Health checking
- Failover support

### 📡 **Client Library**

- Native FastMCP client
- Streaming response handling
- Connection management
- Error handling and retries

## 📁 File Structure

```
fastmcp_custom/
├── server.py          # FastMCP 2.0 HTTP streaming server
├── client.py          # FastMCP 2.0 client library
├── config.py          # Configuration management
├── test_fastmcp.py    # Comprehensive test suite
├── __init__.py        # Package initialization
└── README.md          # This file
```

## 🚀 Quick Start

### 1. Basic HTTP Streaming Server

```bash
# Start HTTP streaming server on port 3000
python fastmcp_custom/server.py --transport streamable-http --port 3000

# With verbose logging
python fastmcp_custom/server.py --transport streamable-http --port 3000 --verbose
```

### 2. Server-Sent Events (Legacy)

```bash
# Use SSE transport (legacy)
python fastmcp_custom/server.py --transport sse --port 3000
```

### 3. STDIO Transport (Claude Desktop Compatible)

```bash
# Use STDIO for Claude Desktop
python fastmcp_custom/server.py --transport stdio
```

### 4. Client Usage

```bash
# Test the FastMCP client
python test_fastmcp_client.py
```

## 🔧 Configuration

### Environment Variables

```bash
# Server configuration
export FASTMCP_HOST="127.0.0.1"
export FASTMCP_PORT="3000"
export FASTMCP_TRANSPORT="streamable-http"

# Authentication (when implemented)
export FASTMCP_ENABLE_AUTH="true"
export FASTMCP_AUTH_TOKEN="your-secret-token"
```

### Programmatic Configuration

```python
from fastmcp_custom.config import config

# Customize settings
config.host = "127.0.0.1"
config.port = 3000
config.transport = "streamable-http"
```

## 🌟 Key Features

### HTTP Streaming Transport

- **MCP Protocol over HTTP**: All communication uses proper MCP protocol
- **Streamable HTTP**: Modern streaming transport (recommended)
- **Server-Sent Events**: Legacy SSE support
- **Connection management**: Automatic session handling

### Available Transports

```python
# Modern streaming (recommended)
transport = "streamable-http"

# Legacy Server-Sent Events
transport = "sse"

# Local/Claude Desktop
transport = "stdio"
```

## 🧪 Testing

### Run Client Tests

```bash
# Make sure server is running first:
python fastmcp_custom/server.py --transport streamable-http --port 3000

# Then test the client:
python test_fastmcp_client.py
```

### Expected Output

```
🧪 Testing FastMCP 2.0 Client Connection
==================================================
✅ Connected to FastMCP server
📋 Listing tools...
✅ Found 28 tools
🧪 Testing get_sites tool...
✅ get_sites completed successfully!
📄 Full result: Name: Default, LiveUrl: localhost, IsOffline: False
```

## 🔄 Integration with Existing Architecture

This FastMCP 2.0 implementation **complements** your existing setup:

### Current Architecture Remains

- ✅ `tahubu_sf/` - Your 28 MCP tools (unchanged)
- ✅ `fastapi_server/` - Traditional REST API (unchanged)
- ✅ `run.py` - STDIO transport for Claude Desktop (unchanged)

### New FastMCP 2.0 Layer

- 🆕 `fastmcp_custom/server.py` - Advanced HTTP streaming server
- 🆕 `test_fastmcp_client.py` - Client testing and examples
- 🆕 Enhanced capabilities: HTTP streaming, future auth/proxying

## 🎯 Use Cases

### 1. **Claude Desktop Integration** (Existing)

```json
{
    "mcpServers": {
        "TahubuSF": {
            "command": "python",
            "args": ["run.py"]
        }
    }
}
```

### 2. **HTTP Streaming Access** (FastMCP 2.0)

```python
from fastmcp import Client

# Connect to FastMCP 2.0 HTTP server
client = Client("http://127.0.0.1:3000/mcp")

async with client:
    # List available tools
    tools = await client.list_tools()
    
    # Call tools using MCP protocol
    sites = await client.call_tool("get_sites")
    blog_posts = await client.call_tool("get_blog_posts")
```

### 3. **Server-to-Server Communication**

```python
from fastmcp import Client

# Connect to remote FastMCP server
client = Client("http://remote-server:3000/mcp")

async with client:
    # Use tools remotely via MCP protocol
    news = await client.call_tool("get_news")
    pages = await client.call_tool("get_pages")
```

## 🌐 Server Information

### MCP Endpoint

- **Primary endpoint**: `http://127.0.0.1:3000/mcp`
- **Protocol**: MCP (Model Context Protocol) over HTTP
- **Transport**: Streamable HTTP (recommended) or SSE (legacy)

### Server Logs

The server provides detailed logging showing:
- Session creation and management
- MCP request processing
- Tool execution results
- Connection lifecycle

Example server output:
```
INFO - Starting MCP server 'TahubuSFAPI FastMCP 2.0' with transport 'streamable-http' on http://127.0.0.1:3000/mcp
INFO - Created new transport with session ID: abc123...
INFO - Processing request of type ListToolsRequest
INFO - Processing request of type CallToolRequest
```

## 🔄 Migration Path

### Phase 1: Current State ✅

1. ✅ Keep existing `run.py` for Claude Desktop
2. ✅ Keep existing `fastapi_server/` for REST API
3. ✅ Added `fastmcp_custom/` for HTTP streaming

### Phase 2: Testing & Validation ✅

1. ✅ HTTP streaming transport working
2. ✅ All 28 tools accessible via FastMCP
3. ✅ Client library functional

### Phase 3: Future Enhancements

1. 🔄 Implement authentication features
2. 🔄 Add proxy server capabilities
3. 🔄 Deploy with monitoring and scaling

## 🛠️ Advanced Usage

### Custom Client Implementation

```python
import asyncio
from fastmcp import Client

async def use_tahubu_tools():
    client = Client("http://127.0.0.1:3000/mcp")
    
    async with client:
        # Get all available tools
        tools = await client.list_tools()
        print(f"Available tools: {len(tools)}")
        
        # Use specific tools
        sites = await client.call_tool("get_sites")
        blog_posts = await client.call_tool("get_blog_posts", {"limit": 10})
        
        return sites, blog_posts

# Run the client
sites, posts = asyncio.run(use_tahubu_tools())
```

### Server Startup Options

```bash
# Basic startup
python fastmcp_custom/server.py --transport streamable-http --port 3000

# With verbose logging
python fastmcp_custom/server.py --transport streamable-http --port 3000 --verbose

# Different port
python fastmcp_custom/server.py --transport streamable-http --port 4000

# STDIO mode (for Claude Desktop)
python fastmcp_custom/server.py --transport stdio
```

## 📚 Technical Details

### MCP Protocol Implementation

- Uses proper MCP (Model Context Protocol) specification
- Supports all standard MCP request types:
  - `ListToolsRequest` - Get available tools
  - `CallToolRequest` - Execute tools
  - `ListResourcesRequest` - Get resources
  - `ReadResourceRequest` - Read resource content

### Transport Layer

- **Streamable HTTP**: Modern, efficient streaming transport
- **Session Management**: Automatic session creation and cleanup
- **Error Handling**: Proper MCP error responses
- **Connection Lifecycle**: Clean connection setup/teardown

## 🎉 Benefits Summary

✅ **Maintains Compatibility**: All existing tools work unchanged  
✅ **Adds HTTP Access**: Stream MCP tools over HTTP  
✅ **Production Foundation**: Built on FastMCP 2.0 framework  
✅ **Easy Integration**: Drop-in addition to existing setup  
✅ **Future Ready**: Foundation for auth, proxying, scaling  

Your TahubuSF project now has both traditional MCP capabilities AND modern HTTP streaming access! 🚀

## 🔍 Troubleshooting

### Common Issues

1. **"Unknown transport: http"** - Use `streamable-http` instead of `http`
2. **404 errors on endpoints** - Use the MCP endpoint `/mcp`, not REST endpoints
3. **Client connection issues** - Ensure server URL includes `/mcp` path
4. **Import errors** - Make sure FastMCP 2.0 is installed: `pip install fastmcp`

### Verification Steps

1. Start server: `python fastmcp_custom/server.py --transport streamable-http --port 3000`
2. Test client: `python test_fastmcp_client.py`
3. Check server logs for session creation and request processing
4. Verify all 28 tools are accessible via the client 