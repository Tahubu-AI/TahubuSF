![TahubuSF](media/tahubusf-light.svg)

# TahubuSF MCP Server

A Model Context Protocol (MCP) server that provides seamless access to **Sitefinity CMS** data and operations. Built with FastMCP 2.x, it offers both MCP integration for Claude Desktop and REST API access for web applications.

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

### 4. Authentication Configuration

Sitefinity web services require authentication for most operations. TahubuSF supports three authentication methods:

#### Anonymous Access

For public content or services that don't require authentication:

```bash
SITEFINITY_AUTH_TYPE=anonymous
```

#### API Key Authentication

For web services configured with API key access:

```bash
SITEFINITY_AUTH_TYPE=apikey
SITEFINITY_API_KEY=your-api-key-from-sitefinity
```

In Sitefinity, generate an API key at: Administration → Settings → Advanced → WebServices → WebServiceAccessKey

#### Access Key

For user-specific authentication:

```bash
SITEFINITY_AUTH_TYPE=accesskey
SITEFINITY_AUTH_KEY=your-access-key
```

In Sitefinity, you can generate an Access Key by following these steps:

1. Create a user with appropriate permissions for the web service
2. Navigate to Administration → Users
3. Click Actions → Generate access key for the specific user
4. Copy the key immediately (it will only be shown once)

For more details, see [Sitefinity's official documentation on generating access keys](https://www.progress.com/documentation/sitefinity-cms/generate-access-key).

Choose the appropriate authentication method based on your Sitefinity's web services configuration:

- For "Anonymous users", use `anonymous`
- For "API key authentication", use `apikey` 
- For "Authenticated users", use `accesskey`

### 5. FastAPI Dependencies (for Azure Deployment)

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

## 🚀 Quick Start

### For Claude Desktop (MCP Integration)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start MCP server
python run.py

# 3. Add to Claude Desktop config
```

### For Web/API Access

Start the FastAPI server to access tools via HTTP API:

```bash
# Production/Standard Use
cd fastapi_server
python run.py

# Development/Testing (auto-opens browser to Inspector)
python run_fastapi_dev.py
```

The `run_fastapi_dev.py` script provides the easiest way to get started - it automatically:
- Installs dependencies if needed
- Starts the FastAPI server  
- Opens your browser to the Inspector interface
- Handles cleanup when you stop the server

#### API Endpoints

Once the FastAPI server is running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Tool Inspector**: http://localhost:8000/inspector/
- **Health Check**: http://localhost:8000/health
- **Run Tools**: http://localhost:8000/api/run-tool

#### Inspector Interface

The web interface provides an easy way to test your MCP tools:

- `inspector/index.html`: Main testing interface
- `inspector/css/styles.css`: Styling
- `inspector/js/`: JavaScript modules for tool interaction

## 📋 Available Tools

**28 Sitefinity MCP Tools** including:

### 📰 Content Management

- `getNews` - Get news articles
- `getBlogPosts` - Get blog posts with content
- `getBlogPostById` - Get a specific blog post by its ID
- `getPages` - Get standard pages
- `getSharedContent` - Get shared content blocks

### 📅 Events & Media

- `getEvents` - Get calendar events
- `getCalendars` - Get available calendars
- `getImages` - Get image galleries
- `getDocuments` - Get document libraries

### 🔧 System Operations

- `getSites` - Get site information
- `getForms` - Get available forms
- `getUsers` - Get user accounts
- `searchContent` - Search across content types

### 🛠️ Administrative

- `createContent` - Create new content
- `updateContent` - Update existing content
- `deleteContent` - Delete content
- `publishContent` - Publish/unpublish content

[View complete tool list with descriptions →](TOOLS.md)

## 🏗️ Architecture

### STDIO Transport (MCP)

```bash
Claude Desktop → MCP Protocol → STDIO → TahubuSF Server → Sitefinity API
```

### FastAPI Server (HTTP)

```bash
Web Browser → HTTP/REST → FastAPI → TahubuSF Tools → Sitefinity API
```

## ⚙️ Configuration

### Claude Desktop Setup

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

## 🧪 Testing

### Test MCP Server

```bash
# Test server functionality
python -c "from tahubu_sf.app import create_app; app = create_app(); print('✅ MCP Server Working!')"

# Test STDIO transport
python run.py --verbose
```

### Test FastAPI Server

```bash
# Automated testing
python fastapi_http_test.py

# Manual API testing
curl http://localhost:8000/health
curl http://localhost:8000/api/list-tools
```

## 📂 Project Structure

```
## Project Structure

```
├── tahubu_sf/           # Core library package
│   ├── api/             # API endpoint modules
│   │   ├── blog_posts.py    # Blog post management endpoints
│   │   ├── news.py          # News-related endpoints
│   │   ├── pages.py         # Pages and templates endpoints
│   │   └── sites.py         # Site information endpoints
│   ├── config/          # Configuration settings
│   │   └── settings.py    # URL and app configuration
│   ├── utils/           # Utility functions
│   │   ├── http.py        # HTTP request utilities
│   │   └── string_utils.py # String manipulation utilities
│   └── app.py           # Application factory
│
├── fastapi_server/      # FastAPI implementation
│   ├── main.py          # FastAPI application definition
│   ├── routes.py        # API route definitions
│   ├── config.py        # Configuration settings
│   ├── wsgi.py          # WSGI entry point
│   ├── azure_deploy.py  # Azure deployment utility
│   └── tests/           # API tests
│
├── inspector/           # Web interface for testing
│   ├── css/             # CSS stylesheets
│   │   └── styles.css   # Main stylesheet
│   ├── js/              # JavaScript files
│   │   ├── utils.js     # Utility functions
│   │   ├── formatters.js # Result formatters
│   │   └── tools.js     # Tool interaction functions
│   └── index.html       # Main HTML page
│
├── media/               # Static media files
├── docs/                # Documentation files
├── run_fastapi_dev.py   # FastAPI development utility to start server and open inspector
├── fastapi_http_test.py # FastAPI HTTP transport and tool testing utility
└── run.py               # Entry point for Claude Desktop
```

## 🚢 Deployment

### Local Development

```bash
# MCP/Claude Desktop
python run.py

# Web/API server and Inspector for development
python run_fastapi_dev.py

# Web/API production server
cd fastapi_server && python run.py
```

### Production (HTTP)

```bash
# FastAPI production server
cd fastapi_server
python run.py --host 0.0.0.0 --port 8000

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment

To deploy the FastAPI server using Docker, create a `Dockerfile` in the `fastapi_server` directory:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/fastapi_server
CMD ["python", "run.py", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔍 API Documentation

When running the FastAPI server, comprehensive API documentation is available at:

- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Tool Inspector**: http://localhost:8000/inspector/

## 🛠️ Development

### Adding New Tools

1. Create tool function in `tahubu_sf/api/`
2. Add MCP tool wrapper in `tahubu_sf/tools/`
3. Register tool in `tahubu_sf/app.py`
4. Test with both STDIO and FastAPI

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📚 Documentation

- [Transport Guide](TRANSPORT_GUIDE.md) - STDIO vs HTTP transport
- [Tool Reference](TOOLS.md) - Complete tool documentation  
- [API Guide](API_GUIDE.md) - Sitefinity API integration
- [Claude Desktop Setup](CLAUDE_DESKTOP_FIX.md) - Configuration guide

## 🐛 Troubleshooting

### Common Issues

**Claude Desktop Connection**

- Verify JSON configuration syntax
- Check file paths (use double backslashes on Windows)
- Ensure `uv` is installed and accessible

**FastAPI Server**

- Check port availability with `netstat -an | findstr :8000`
- Verify Sitefinity API connectivity
- Review server logs for detailed errors

**Dependencies**

- Run `pip install -r requirements.txt`
- For `uv`: Run `uv sync` to ensure consistency

### Support

- Check [Issues](https://github.com/your-repo/issues) for known problems
- Create new issue with detailed error information
- Include system details and configuration

---

**Ready to integrate Sitefinity with Claude Desktop and web applications!** 🎉