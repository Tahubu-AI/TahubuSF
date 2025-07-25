# Environment Variables

This document describes the environment variables used in TahubuSF across all server implementations.

## Core Variables

| Variable | Description | Default | Used By |
|----------|-------------|---------|---------|
| `SITEFINITY_SITE_PREFIX` | Base URL for the Sitefinity site | https://thetrainingboss.com | All server implementations |

## Authentication Variables

| Variable | Description | Default | Used By |
|----------|-------------|---------|---------|
| `SITEFINITY_AUTH_TYPE` | Authentication type for Sitefinity API (anonymous, apikey, accesskey) | anonymous | All server implementations |
| `SITEFINITY_API_KEY` | API key for Sitefinity API when using apikey auth type | None | All server implementations |
| `SITEFINITY_AUTH_KEY` | Access Key for Sitefinity API when using accesskey auth type | None | All server implementations |

## Retry Strategy Variables

| Variable | Description | Default | Used By |
|----------|-------------|---------|---------|
| `RETRY_MAX_ATTEMPTS` | Maximum number of retry attempts for API calls | 3 | All server implementations |
| `RETRY_MIN_SECONDS` | Minimum wait time (in seconds) between retries | 1 | All server implementations |
| `RETRY_MAX_SECONDS` | Maximum wait time (in seconds) between retries | 5 | All server implementations |

## Server-Specific Variables

### Simple Server

| Variable | Description | Default | 
|----------|-------------|---------|
| `PORT` | Port for the simple HTTP server | 7777 |
| `HOST` | Host for the simple HTTP server | localhost |

### FastAPI Server

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port for the FastAPI server | 8000 |
| `HOST` | Host for the FastAPI server | 0.0.0.0 |
| `LOG_LEVEL` | Logging level | info |
| `CORS_ORIGINS` | CORS allowed origins | * |
| `API_VERSION` | API version | 1.0.0 |
| `APPINSIGHTS_INSTRUMENTATIONKEY` | Azure Application Insights key | None |

## Setting Environment Variables

### Using .env File (Recommended)

Create a `.env` file in the project root with your configuration:

```
# Core settings
SITEFINITY_SITE_PREFIX=https://your-sitefinity-site.com

# Authentication settings - choose one approach:

# Option 1: Anonymous access (default)
SITEFINITY_AUTH_TYPE=anonymous

# Option 2: API key authentication (for web services)
# SITEFINITY_AUTH_TYPE=apikey
# SITEFINITY_API_KEY=your-api-key

# Option 3: Access Key (for user-specific auth)
# SITEFINITY_AUTH_TYPE=accesskey
# SITEFINITY_AUTH_KEY=your-access-key

# Retry strategy settings
RETRY_MAX_ATTEMPTS=3
RETRY_MIN_SECONDS=1
RETRY_MAX_SECONDS=5

# Server settings
PORT=7777
```

### Using System Environment Variables

You can also set environment variables at the system level or when running commands:

```bash
# Windows PowerShell
$env:SITEFINITY_SITE_PREFIX="https://your-sitefinity-site.com"
$env:SITEFINITY_AUTH_TYPE="apikey"
$env:SITEFINITY_API_KEY="your-api-key"
$env:RETRY_MAX_ATTEMPTS="3"
python run_fastapi_dev.py

# Linux/macOS
SITEFINITY_SITE_PREFIX="https://your-sitefinity-site.com" SITEFINITY_AUTH_TYPE="apikey" SITEFINITY_API_KEY="your-api-key" RETRY_MAX_ATTEMPTS="3" python run_fastapi_dev.py
```

## Environment Variables in Azure

When deploying to Azure App Service, set these environment variables in the application settings:

```
SITEFINITY_SITE_PREFIX=https://your-sitefinity-site.com
SITEFINITY_AUTH_TYPE=apikey
SITEFINITY_API_KEY=your-api-key
RETRY_MAX_ATTEMPTS=3
RETRY_MIN_SECONDS=1
RETRY_MAX_SECONDS=5
WEBSITES_PORT=8000
```
