# TahubuSF MCP Server Transport Guide

## Overview

Your TahubuSF MCP server has been successfully upgraded to use **FastMCP 2.0**, which provides multiple transport protocols for different deployment scenarios. This guide explains how to use each transport option.

## What Changed

### Before (MCP SDK FastMCP 1.0)
```python
from mcp.server.fastmcp import FastMCP  # Official MCP SDK
mcp.run()                               # STDIO only
```

### After (FastMCP 2.0 - Now Working!)
```python
from fastmcp import FastMCP             # Standalone FastMCP 2.0
mcp.run(transport="stdio")              # STDIO transport (default)
mcp.run(transport="sse")                # SSE transport for web clients
mcp.run(transport="streamable-http")    # Modern HTTP transport
```

## Available Transport Protocols

### 1. 🔌 STDIO Transport (Default)

**Status**: ✅ **Working and Stable**

**Best for**: Local development, Claude Desktop integration

**Usage**:
```bash
# Default - no arguments needed
python run.py

# Explicitly specify STDIO
python run.py --transport stdio
```

**Claude Desktop Configuration**:
```json
{
    "mcpServers":{
        "TahubuSF": {
            "command": "uv",
            "args": [
                "--directory",
                "D:\\repos\\TahubuSF",
                "run",
                "run.py"
            ]
        }
    }
}
```

### 2. 🌐 SSE Transport (Server-Sent Events)

**Status**: ✅ **Working and Ready**

**Best for**: Web-based MCP clients, legacy SSE support

**Usage**:
```bash
# Start SSE server
python run.py --transport sse --port 5000

# Custom host and port
python run.py --transport sse --host 0.0.0.0 --port 8080
```

**Claude Desktop Configuration**:
```json
{
    "mcpServers":{
        "TahubuSF-SSE": {
            "url": "http://127.0.0.1:5000/sse"
        }
    }
}
```

### 3. 🚀 Streamable HTTP Transport (Recommended for Web)

**Status**: ✅ **Working and Production-Ready**

**Best for**: Modern web deployments, production environments

**Usage**:
```bash
# Start HTTP server
python run.py --transport streamable-http --port 5000 --path /mcp

# Custom configuration
python run.py --transport streamable-http --host 0.0.0.0 --port 3000 --path /api/mcp
```

**Claude Desktop Configuration**:
```json
{
    "mcpServers":{
        "TahubuSF-HTTP": {
            "url": "http://127.0.0.1:5000/mcp"
        }
    }
}
```

## Command Line Options

The `run.py` script now supports comprehensive command line options:

```bash
python run.py --help
```

**Available Options**:
- `--transport {stdio,sse,streamable-http}`: Transport protocol (default: stdio)
- `--host HOST`: Host to bind to for web transports (default: 127.0.0.1)
- `--port PORT`: Port to bind to for web transports (default: 5000)  
- `--path PATH`: Path for HTTP transport (default: /sse)
- `--verbose, -v`: Enable verbose logging

## Examples

### Development Scenarios

```bash
# Local development with Claude Desktop
python run.py

# Test web interface with SSE
python run.py --transport sse --port 5000

# Production-ready HTTP server
python run.py --transport streamable-http --port 8080 --host 0.0.0.0
```

### Production Deployment

```bash
# For Docker containers
python run.py --transport streamable-http --host 0.0.0.0 --port 8000 --path /mcp

# For cloud deployments with custom paths
python run.py --transport streamable-http --port 3000 --path /api/v1/mcp
```

## Testing Your Setup

Use the provided test scripts to verify your setup:

```bash
# Test all transports
python test_transports.py

# Interactive demo
python demo_transports.py
```

## Deployment Recommendations

| Scenario | Recommended Transport | Configuration |
|----------|----------------------|---------------|
| **Local Development** | STDIO | Default `python run.py` |
| **Claude Desktop** | STDIO | Command-based config |
| **Web Testing** | SSE | `--transport sse` |
| **Production Web** | Streamable HTTP | `--transport streamable-http` |
| **Docker/Cloud** | Streamable HTTP | With `--host 0.0.0.0` |

## Migration Notes

### Dependencies Updated
- Added `fastmcp>=2.6.0` to requirements.txt
- Updated to `mcp>=1.9.0` (compatible version with ProgressFnT)
- All 27 existing tools continue to work unchanged

### Code Changes
- Updated import in `tahubu_sf/app.py` to `from fastmcp import FastMCP`
- Enhanced `run.py` with full transport options
- Added comprehensive documentation and examples

### No Breaking Changes
- Existing STDIO functionality works exactly as before
- All MCP tools function identically
- Enhanced with new transport capabilities

## Troubleshooting

### ✅ Current Working State

1. **Test Server Creation**:
   ```bash
   python -c "from tahubu_sf.app import create_app; app = create_app(); print('✅ Working!')"
   ```

2. **Test STDIO Transport**:
   ```bash
   python run.py --verbose
   ```

3. **Test SSE Transport**:
   ```bash
   python run.py --transport sse --port 5000 --verbose
   # Then test: curl -I http://127.0.0.1:5000/sse
   ```

4. **Test HTTP Transport**:
   ```bash
   python run.py --transport streamable-http --port 5001 --path /mcp
   # Then test: curl -I http://127.0.0.1:5001/mcp
   ```

### 🔧 Common Issues

1. **Port Already in Use**
   ```bash
   # Use a different port
   python run.py --transport sse --port 5001
   ```

2. **Host Binding Issues**
   ```bash
   # Bind to all interfaces for remote access
   python run.py --transport streamable-http --host 0.0.0.0
   ```

3. **Path Conflicts**
   ```bash
   # Use custom path
   python run.py --transport streamable-http --path /custom/mcp
   ```

### 🎯 Success Criteria

All transport protocols are now working:
- ✅ **STDIO Transport**: Perfect for Claude Desktop integration  
- ✅ **SSE Transport**: Working with HTTP/1.1 200 OK response
- ✅ **HTTP Transport**: Working with proper redirects and endpoints
- ✅ **All 27 MCP Tools**: Available across all transport protocols

## Current Benefits

✅ **Multi-Transport Support**: All three transport protocols working  
✅ **Modern Architecture**: FastMCP 2.0 with latest features  
✅ **Production Ready**: Suitable for web deployments  
✅ **Claude Desktop**: Seamless STDIO integration  
✅ **Web Integration**: SSE and HTTP for browser-based clients  
✅ **Scalability**: Host and port configuration for different environments

Your TahubuSF MCP server now has the full FastMCP 2.0 capabilities with multiple transport support! 🎉 