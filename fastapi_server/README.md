# TahubuSF FastAPI Server

A production-ready FastAPI implementation of the TahubuSF Sitefinity MCP tools server with Azure App Service deployment support.

## Features

- Modern FastAPI web server with async/await support
- Structured API with proper request/response models
- Swagger UI documentation at `/docs`
- Clean separation of concerns (routes, config, etc.)
- Azure App Service deployment ready
- Production WSGI setup with Gunicorn
- Health checks for monitoring
- Configurable CORS support
- Automated testing support

## Project Structure

```
fastapi_server/
├── __init__.py           # Package initialization
├── config.py             # Configuration settings
├── main.py               # FastAPI application definition
├── routes.py             # API route definitions
├── wsgi.py               # WSGI entry point for Gunicorn
├── azure_deploy.py       # Azure deployment utility
├── README.md             # This file
└── tests/                # Test directory
    ├── __init__.py
    └── test_api.py       # API tests
```

## Getting Started

### Running Locally

To run the server locally:

```bash
python run_fastapi.py --port 8000
```

Or directly:

```bash
cd fastapi_server
uvicorn main:app --reload
```

### API Documentation

Once running, access the Swagger UI documentation at:

```
http://localhost:8000/docs
```

## Azure Deployment

### Using the Deployment Script

The server includes a deployment utility that can automate the Azure App Service setup:

```bash
python -m fastapi_server.azure_deploy --app-name YourAppName
```

### Manual Deployment

Follow these steps to deploy manually:

1. Create Azure resources (Resource Group, App Service Plan, Web App)
2. Configure the Web App:
   - Set the startup command to use Gunicorn
   - Configure environment variables
3. Deploy the code using Git deployment or Azure DevOps

See [Azure deployment documentation](https://learn.microsoft.com/azure/app-service/quickstart-python) for more details.

## Configuration

The server can be configured using environment variables or a `.env` file at the project root:

### Core Variables

- `SITEFINITY_SITE_PREFIX`: Base URL for the Sitefinity site (default: https://thetrainingboss.com)

### Authentication Variables

- `SITEFINITY_AUTH_TYPE`: Authentication type to use (anonymous, apikey, accesskey)
- `SITEFINITY_API_KEY`: API key when using apikey auth type
- `SITEFINITY_AUTH_KEY`: Access Key when using accesskey auth type

### FastAPI Specific Variables

- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: info)
- `CORS_ORIGINS`: CORS allowed origins (default: *)
- `APPINSIGHTS_INSTRUMENTATIONKEY`: Azure Application Insights key

### Environment Variables for Azure

When deploying to Azure App Service, you must set these environment variables in the application settings:

```
SITEFINITY_SITE_PREFIX=https://your-sitefinity-site.com
SITEFINITY_AUTH_TYPE=apikey  # Choose appropriate auth type
SITEFINITY_API_KEY=your-api-key  # If using apikey auth
WEBSITES_PORT=8000
```

For more details on environment variables, see [Environment Variables Documentation](../ENV_VARIABLES.md).

## Testing

Run tests using pytest:

```bash
python test_fastapi.py
```
