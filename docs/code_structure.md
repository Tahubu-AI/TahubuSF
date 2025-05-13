# TahubuSF Code Structure Guidelines

This document outlines the recommended structure for organizing code in the TahubuSF MCP server project.

## Package Structure

The project follows a modular structure:

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