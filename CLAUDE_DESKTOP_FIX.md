# Claude Desktop Dependency Issue - RESOLVED ✅

## Problem Description

When using `uv run run.py` in Claude Desktop, the MCP server was failing with:
```
ImportError: cannot import name 'ProgressFnT' from 'mcp.shared.session'
```

## Root Cause

The issue was caused by conflicting dependency specifications:

1. **requirements.txt** specified `mcp>=1.9.0` and `fastmcp>=2.6.0` (correct versions)
2. **pyproject.toml** specified `mcp[cli]>=1.8.0` (outdated version)

When Claude Desktop ran `uv run run.py`, uv used the pyproject.toml dependencies, which forced MCP back to version 1.8.0. This older version doesn't have the `ProgressFnT` type that FastMCP 2.x requires.

## Solution Applied

### 1. Updated pyproject.toml Dependencies

Fixed the dependency conflict by updating `pyproject.toml` to match the working `requirements.txt`:

```toml
[project]
dependencies = [
    "httpx>=0.28.1",
    "mcp>=1.9.0",              # ✅ Updated from 1.8.0
    "python-dotenv>=1.0.0",
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.6.0",
    "tenacity>=8.2.3",
    "fastmcp>=2.6.0",          # ✅ Added FastMCP 2.x
    "requests>=2.31.0",
]
```

### 2. Synchronized Dependencies

Ran `uv sync` to ensure all dependencies are properly resolved and consistent.

## Verified Working Configurations

### Option 1: uv run (Recommended)

Your original configuration now works perfectly:

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

### Option 2: Direct Python (Alternative)

If you prefer direct Python execution:

```json
{
    "mcpServers":{
        "TahubuSF": {
            "command": "D:\\repos\\TahubuSF\\.venv\\Scripts\\python.exe",
            "args": [
                "D:\\repos\\TahubuSF\\run.py"
            ]
        }
    }
}
```

## Test Results

✅ **uv run run.py** - Working  
✅ **python run.py** - Working  
✅ **FastMCP 2.x imports** - Working  
✅ **All transport protocols** - Working  
✅ **27 MCP tools** - Working  

## Key Benefits Restored

- **STDIO Transport**: Perfect for Claude Desktop
- **SSE Transport**: Available for web clients  
- **HTTP Transport**: Ready for production deployments
- **FastMCP 2.x Features**: LLM sampling, context injection, etc.

## Prevention

This issue was resolved by ensuring that:
1. Both `requirements.txt` and `pyproject.toml` specify the same dependency versions
2. `uv sync` is run after any dependency changes
3. The virtual environment is properly maintained

Your TahubuSF MCP server is now fully compatible with Claude Desktop and all transport protocols! 🎉 