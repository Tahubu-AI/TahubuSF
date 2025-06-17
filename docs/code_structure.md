# TahubuSF Code Structure Guidelines

This document outlines the recommended structure for organizing code in the TahubuSF MCP server project.

## Package Structure

```
TahubuSF/
├── tahubu_sf/
│   ├── __init__.py
│   ├── app.py                 # Main FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   ├── blog_posts.py      # Blog post management endpoints
│   │   ├── news.py           # News item management endpoints
│   │   ├── lists.py          # List item management endpoints
│   │   ├── events.py         # Event management endpoints
│   │   ├── pages.py          # Page management endpoints
│   │   ├── images.py         # Image management endpoints
│   │   ├── documents.py      # Document management endpoints
│   │   ├── videos.py         # Video management endpoints
│   │   └── shared_content.py # Shared content management endpoints
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Configuration settings
│   ├── utils/
│   │   ├── __init__.py
│   │   └── http.py          # HTTP utility functions
│   └── fastapi/
│       ├── __init__.py
│       └── routes.py        # FastAPI route definitions
├── fastapi_server/
│   ├── __init__.py
│   ├── main.py             # FastAPI server entry point
│   └── routes.py           # FastAPI route handlers
├── fastmcp_custom/
│   ├── __init__.py
│   ├── server.py           # FastMCP server implementation
│   └── client.py           # FastMCP client implementation
├── inspector/
│   ├── index.html         # Inspector web interface
│   ├── css/
│   │   └── styles.css     # Inspector styles
│   └── js/
│       ├── tools.js       # Tool interaction functions
│       ├── formatters.js  # Result formatting functions
│       └── utils.js       # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_blog_post.py  # Blog post tests
│   └── test_news.py       # News item tests
├── docs/
│   └── code_structure.md  # This file
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Key Components

### API Layer (`tahubu_sf/api/`)

- `blog_posts.py`: Handles blog post operations (create, read, update, delete)
- `news.py`: Manages news item operations
- `lists.py`: Handles list item operations
- `events.py`: Manages event operations
- `pages.py`: Handles page operations
- `images.py`: Manages image operations
- `documents.py`: Handles document operations
- `videos.py`: Manages video operations
- `shared_content.py`: Handles shared content operations

### Server Layer

- `fastapi_server/`: FastAPI server implementation
- `fastmcp_custom/`: FastMCP server and client implementation

### Inspector Interface

- `inspector/`: Web-based interface for testing and debugging
  - `index.html`: Main interface
  - `js/tools.js`: Tool interaction logic
  - `js/formatters.js`: Result formatting
  - `js/utils.js`: Utility functions

### Configuration

- `config/settings.py`: Central configuration management
- `utils/http.py`: HTTP utility functions

### Testing

- `tests/`: Test suite for API endpoints
  - `test_blog_post.py`: Blog post tests
  - `test_news.py`: News item tests

## Guidelines for Adding New Functionality

### 1. API Endpoints

New API endpoints should:

- Be placed in the appropriate module under `tahubu_sf/api/`
- Be organized by domain (e.g., blogs, news, pages)
- Use the utility functions from `tahubu_sf/utils/` for HTTP requests
- Have comprehensive docstrings explaining their purpose and return values

Example:

```python
"""
API endpoint for [domain]
"""
from tahubu_sf.config.settings import ENDPOINTS
from tahubu_sf.utils.http import make_request

async def get_something() -> str:
    """
    Get something from the Sitefinity site.
    
    Returns:
        str: A formatted string containing details
    """
    data = await make_request(ENDPOINTS["endpoint_key"])
    
    # Process data
    return processed_data
```

### 2. Configuration

- URLs and other configuration should be defined in `tahubu_sf/config/settings.py`
- Environment-specific configuration should use environment variables
- Add new API endpoints to the `ENDPOINTS` dictionary

### 3. Utility Functions

- Common functionality should be extracted to utilities
- Place utilities in the appropriate module under `tahubu_sf/utils/`
- Write utilities to be reusable across different API endpoints

### 4. Registering New Tools

After creating a new API endpoint function, register it in `tahubu_sf/app.py`:

```python
from tahubu_sf.api.new_module import get_something

def create_app() -> FastMCP:
    app = FastMCP(APP_NAME)
    
    # Register API tools
    # ... existing tools ...
    app.tool()(get_something)
    
    return app
```

## Best Practices

1. **Error Handling**: Use try/except blocks and log errors appropriately
2. **Type Hints**: Use Python type hints for function parameters and return values
3. **Documentation**: Write clear docstrings for all functions and modules
4. **Testing**: Write tests for new functionality
5. **Logging**: Use the logging module instead of print statements

## Development Workflow

1. Create a new branch for your feature
2. Implement the feature following the structure guidelines
3. Add appropriate tests
4. Update documentation if necessary
5. Submit a pull request for review
