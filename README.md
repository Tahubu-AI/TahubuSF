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

fastapi_server/          # FastAPI implementation
├── main.py              # FastAPI application definition
├── routes.py            # API route definitions
├── config.py            # Configuration settings
└── wsgi.py              # WSGI entry point for production
```

## Environment setup

To run the MCP server, you need to have Python 3.13 or higher installed on your machine. You can download it from the official website: [Python Downloads](https://www.python.org/downloads/).

### 1. Create a Virtual Environment

In VS Code, create a new Python environment by opening the terminal and running:

```bash
python -m venv .venv
```

This will create a new virtual environment named `.venv`. Activate the virtual environment:

- On Windows:

```bash
.venv\Scripts\Activate.ps1
```

- On macOS and Linux:

```bash
source .venv/bin/activate
```

You should see `(.venv)` or `(tahubusf)` at the beginning of your terminal prompt, indicating you're working within the virtual environment.

### 2. Install Dependencies

#### Using uv (recommended):

First, install `uv` by following the instructions in the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

Then install the dependencies:

```bash
uv pip install -r requirements.txt
```

#### Using pip:

```bash
pip install -r requirements.txt
```

### 3. FastAPI Dependencies (for Azure Deployment)

If you plan to use the FastAPI server for Azure deployment, install the additional dependencies:

```bash
# Within your activated virtual environment:
uv pip install fastapi uvicorn[standard] pydantic
```

Or if using pip:

```bash
# Within your activated virtual environment:
pip install -r requirements.txt
pip install fastapi uvicorn[standard] pydantic
```

### Troubleshooting Dependencies

If you encounter dependency conflicts with packages like LangChain, try these solutions:

1. Create a separate virtual environment for this project:
   ```bash
   python -m venv fresh_venv
   .\fresh_venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Use `--no-deps` flag to avoid dependency resolution conflicts:
   ```bash
   pip install --force-reinstall fastapi==0.110.0 uvicorn[standard]==0.27.0 pydantic==2.6.0 --no-deps
   ```

3. Ensure the correct Python interpreter is being used in VS Code by selecting it from the Python interpreter list.

## Running the Server

### Local Development (simple_server.py)

For quick, reliable local development and testing:

```bash
python simple_server.py
```

This starts a custom HTTP server built with Python's standard library that:

- Requires minimal dependencies (avoids MCP tooling conflicts)
- Serves a web interface for testing all Sitefinity MCP tools
- Directly executes MCP tools with your modular code structure
- Opens your browser automatically to the testing interface
- Is extremely reliable across different Python environments

The simple server is the recommended way to test your code during development, as it avoids the dependency and environment issues sometimes encountered with the MCP development tools.

### Azure-Ready Server (FastAPI)

For production deployment to Azure App Service:

```bash
# First, ensure you're in the activated virtual environment
# and have installed the FastAPI dependencies

python run_fastapi.py
```

The FastAPI implementation offers:

- Production-ready API with Swagger documentation
- Azure App Service deployment support
- Proper request/response models with validation
- Detailed error handling and logging
- CORS and security configuration options

```bash
python run_fastapi.py --port 9000
```

### Claude Desktop Integration (run.py)

For direct integration with Claude Desktop:

```bash
python run.py
```

This runs the server with stdio transport using the modular code structure from the `tahubu_sf` package.

## Server Comparison

| Feature | simple_server.py | FastAPI Server |
|---------|------------------|----------------|
| **Purpose** | Local development & testing | Production & cloud deployment |
| **Dependencies** | Minimal (Python stdlib) | FastAPI ecosystem (multiple packages) |
| **Reliability** | Very high, minimal points of failure | Good, but more dependencies |
| **Features** | Basic testing interface | Production API, Swagger UI, request validation |
| **Deployment** | Local use only | Azure App Service ready |
| **Best for** | Quick testing, avoiding dependency issues | Cloud deployment, API consumption |

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
5. Add it to both `simple_server.py` and `fastapi_server/routes.py` to make it available in both interfaces

For more details, see [Code Structure Guidelines](docs/code_structure.md).

## FastAPI Server Details

For more details on the FastAPI implementation that can be deployed to Azure App Service, see [FastAPI Server Documentation](fastapi_server/README.md).
