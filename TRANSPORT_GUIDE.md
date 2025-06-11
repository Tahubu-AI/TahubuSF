# TahubuSF Server Transport Guide

## Overview

The TahubuSF server provides **two reliable deployment options** for different use cases:

1. **🔌 STDIO Transport** - For Claude Desktop and MCP integration  
2. **🚀 FastAPI Server** - For HTTP/web access and production deployments

## Available Transport Options

### 1. 🔌 STDIO Transport (MCP Integration)

**Status**: ✅ **Working and Stable**

**Best for**: Claude Desktop integration, MCP clients

**Usage**:
```bash
# Run MCP server with STDIO transport
python run.py

# With verbose logging
python run.py --verbose
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

### 2. 🚀 FastAPI Server (HTTP/Web Access)

**Status**: ✅ **Working and Production-Ready**

**Best for**: Web deployments, REST API access, production environments

**Usage**:
```bash
# Start FastAPI server on port 8000
cd fastapi_server
python run.py

# Custom port and host
python run.py --port 9000 --host 0.0.0.0
```

**Features**:
- ✅ REST API endpoints for all 28 MCP tools
- ✅ OpenAPI documentation at `/docs`
- ✅ Health check endpoint at `/health`
- ✅ Web inspector UI at `/inspector/`
- ✅ Production-ready with CORS support

## Quick Start Guide

### For Claude Desktop Users
```bash
# 1. Start the MCP server
python run.py

# 2. Add to Claude Desktop config
# (Use the JSON config shown above)
```

### For Web/API Users
```bash
# 1. Start the FastAPI server
cd fastapi_server
python run.py

# 2. Access the API
# • API Docs: http://localhost:8000/docs
# • Health: http://localhost:8000/health
# • Tools: http://localhost:8000/api/run-tool
```

## Testing Your Setup

### Test STDIO (MCP) Transport
```bash
# Test server creation
python -c "from tahubu_sf.app import create_app; app = create_app(); print('✅ MCP Server Working!')"

# Test STDIO transport
python run.py --verbose
```

### Test FastAPI (HTTP) Transport
```bash
# Test FastAPI server and all tools
python fastapi_http_test.py

# Or manually test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/list-tools
```

## Architecture Comparison

| Feature | STDIO Transport | FastAPI Server |
|---------|----------------|----------------|
| **Claude Desktop** | ✅ Perfect | ❌ Not compatible |
| **MCP Clients** | ✅ Native support | ❌ Different protocol |
| **Web Browsers** | ❌ Not accessible | ✅ Full REST API |
| **Production Apps** | ❌ Process-based only | ✅ HTTP/HTTPS ready |
| **Documentation** | MCP protocol | ✅ OpenAPI/Swagger |
| **Authentication** | Process isolation | ✅ Configurable auth |
| **Scalability** | Single process | ✅ Web server scaling |

## Deployment Recommendations

| Scenario | Recommended Solution | Command |
|----------|---------------------|---------|
| **Claude Desktop** | STDIO Transport | `python run.py` |
| **Local Development** | FastAPI Server | `cd fastapi_server && python run.py` |
| **Production Web** | FastAPI Server | `cd fastapi_server && python run.py --host 0.0.0.0` |
| **Docker/Cloud** | FastAPI Server | `cd fastapi_server && python run.py --port $PORT` |
| **Testing/Debugging** | Both available | Use test scripts |

## Migration Notes

### What Changed
- **Simplified**: Removed problematic MCP HTTP transport
- **Reliable**: STDIO transport for MCP, FastAPI for HTTP
- **Cleaner**: Single purpose for each server type
- **Maintained**: All 28 MCP tools work in both options

### No Breaking Changes
- ✅ Existing STDIO functionality unchanged
- ✅ All MCP tools work identically
- ✅ FastAPI server provides equivalent HTTP access
- ✅ Claude Desktop integration unchanged

## Current Benefits

✅ **Dual-Server Architecture**: MCP (STDIO) + Web (FastAPI)  
✅ **Reliable Transports**: No compatibility issues  
✅ **Production Ready**: Both options are deployment-ready  
✅ **Full Tool Access**: All 28 tools available in both modes  
✅ **Clear Separation**: MCP for desktop, HTTP for web  
✅ **Easy Testing**: Dedicated test scripts for both modes

## Troubleshooting

### STDIO Transport Issues
```bash
# Test server creation
python -c "from tahubu_sf.app import create_app; create_app()"

# Check dependencies
pip install -r requirements.txt
```

### FastAPI Server Issues
```bash
# Test FastAPI directly
cd fastapi_server && python -c "from main import app; print('FastAPI OK')"

# Check port availability
netstat -an | findstr :8000
```

### Claude Desktop Issues
1. Verify the JSON configuration syntax
2. Check file paths (use double backslashes on Windows)
3. Ensure `uv` is installed and accessible
4. Test `uv run run.py` manually first

Your TahubuSF server now provides reliable, production-ready access via both MCP and HTTP protocols! 🎉 