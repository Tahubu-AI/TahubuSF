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

### 3. Configure Environment Variables

The TahubuSF application uses environment variables for configuration, the most important being:

- `SITEFINITY_SITE_PREFIX`: Base URL for your Sitefinity site (default: https://thetrainingboss.com)

Set this by creating a `.env` file in the project root:

```
SITEFINITY_SITE_PREFIX=https://your-sitefinity-site.com
```

Or set it in your environment before running any server:

```bash
# Windows PowerShell
$env:SITEFINITY_SITE_PREFIX="https://your-sitefinity-site.com"

# Linux/macOS
export SITEFINITY_SITE_PREFIX="https://your-sitefinity-site.com"
```

For a complete list of environment variables, see [Environment Variables Documentation](ENV_VARIABLES.md).

### 4. FastAPI Dependencies (for Azure Deployment)

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

## Testing & Running Options

This project offers multiple ways to test and run your MCP server, each optimized for different use cases:

### 1. Simple Server (Recommended for Development)

The simplest and most reliable way to test your MCP tools:

```bash
python simple_server.py
```

This starts a custom HTTP server built with Python's standard library that:

- Requires minimal dependencies (avoids MCP tooling conflicts)
- Serves a web interface for testing all Sitefinity MCP tools
- Directly executes MCP tools with your modular code structure
- Opens your browser automatically to the testing interface
- Is extremely reliable across different Python environments

**Best for**: Daily development and testing when you need a stable experience

### 2. FastAPI Server Options

#### Option A: Direct Test Script (Easiest)

For quickly testing the FastAPI server without import path issues:

```bash
python direct_test.py
```

This script:

- Automatically installs required dependencies if needed
- Handles Python path issues automatically
- Opens your browser to the FastAPI server UI
- Shows real-time logs in the console

#### Option B: Standard Entry Point

The standard way to run the FastAPI server:

```bash
python run_fastapi.py [--port PORT] [--host HOST]
```

Example with custom port:

```bash
python run_fastapi.py --port 9000
```

#### Option C: Testing with UI and API Tests

```bash
python test_fastapi.py
```

This runs the FastAPI server, opens a browser, and executes API tests to verify functionality.

### 3. Claude Desktop Integration

For direct integration with Claude Desktop:

```bash
python run.py
```

This runs the server with stdio transport using the modular code structure from the `tahubu_sf` package.

## Entry Points Comparison

| Entry Point | Command | Best For | Pros | Cons |
|-------------|---------|----------|------|------|
| **simple_server.py** | `python simple_server.py` | Local development | • Most reliable<br>• No dependency issues<br>• Simple to use | • Basic UI<br>• Not suitable for production |
| **direct_test.py** | `python direct_test.py` | Testing FastAPI | • Handles import issues<br>• Auto-installs requirements | • Temporary files<br>• More complex |
| **run_fastapi.py** | `python run_fastapi.py` | Azure deployment prep | • Production-quality API<br>• Swagger docs | • More dependencies<br>• Possible import issues |
| **test_fastapi.py** | `python test_fastapi.py` | API validation | • Runs tests automatically<br>• Validates responses | • Focuses on testing |
| **run.py** | `python run.py` | Claude Desktop | • Direct tool execution<br>• MCP integration | • No web interface |

### When to Use Each Option

- **simple_server.py**: When you want reliable, hassle-free testing during development
- **direct_test.py**: When you want to test the FastAPI implementation without dealing with Python path issues
- **run_fastapi.py**: When preparing for Azure deployment or need a production-quality API
- **test_fastapi.py**: When testing API correctness and responses
- **run.py**: When integrating with Claude Desktop

## Claude Desktop Integration

To use the MCP server in Claude desktop, edit the `claude_desktop_config.json` file and include the following:

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

### Quick Testing

To quickly test the FastAPI server without any import path issues, use the direct test script:

```bash
python direct_test.py
```

This is the most reliable way to test the FastAPI server on different Python environments.
