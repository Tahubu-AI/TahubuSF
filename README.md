![TahubuSF](media/tahubusf-light.svg)

# TahubuSF - Sitefinity MCP API Server

An enterprise-grade MCP server for interacting with Sitefinity APIs.

## Project Structure

```
tahubu_sf/
├── api/                  # API endpoint modules
│   ├── blogs.py          # Blog-related endpoints
│   ├── news.py           # News-related endpoints
│   ├── pages.py          # Pages and templates endpoints
│   ├── sites.py          # Site information endpoints
│   └── __init__.py
├── config/               # Configuration settings
│   ├── settings.py       # URL and app configuration
│   └── __init__.py
├── utils/                # Utility functions
│   ├── http.py           # HTTP request utilities
│   └── __init__.py
└── __init__.py
app.py                   # Application factory
run.py                   # Entry point script
```

## Running the Server

### Development Mode (Recommended)

For the easiest and most reliable development experience:

```bash
python simple_server.py
```

This starts a custom HTTP server that:

- Serves a web interface for testing the TahubuSF MCP tools
- Directly executes MCP tools without any dependency issues
- Opens your browser automatically to the testing interface

This development mode uses the well-organized modular code structure from the `tahubu_sf` package.

### Production Mode

For direct integration with Claude Desktop:

```bash
python run.py
```

This runs the server with stdio transport using the modular code structure from the `tahubu_sf` package.

## Claude Desktop Integration

To use the MCP server in Claude desktop, edit the `claude_desktop_config.json` file and include the following:

```json
{
    "mcpServers": {
        "TahubuSFAPI": {
            "command": "python",
            "args": [
                "run.py"
            ],
            "cwd": "D:\\repos\\TahubuSF"
        }
    }
}
```

Replace `D:\\repos\\TahubuSF` with the absolute path to your project directory.

## Development

### Adding New Endpoints

To add a new API endpoint:

1. Create a new module in the `tahubu_sf/api/` directory
2. Add the endpoint URL to `tahubu_sf/config/settings.py`
3. Create your API function using the provided HTTP utilities
4. Register the function in `tahubu_sf/app.py`
5. Add it to `simple_server.py` if you want it available in the development interface

For more details, see [Code Structure Guidelines](docs/code_structure.md).
