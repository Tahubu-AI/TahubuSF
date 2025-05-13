# Environment Variables

This document describes the environment variables used in TahubuSF across all server implementations.

## Core Variables

| Variable | Description | Default | Used By |
|----------|-------------|---------|---------|
| `SITEFINITY_SITE_PREFIX` | Base URL for the Sitefinity site | https://thetrainingboss.com | All server implementations |

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

# Server settings
PORT=7777
```

### Using System Environment Variables

You can also set environment variables at the system level or when running commands:

```bash
# Windows PowerShell
$env:SITEFINITY_SITE_PREFIX="https://your-sitefinity-site.com"
python simple_server.py

# Linux/macOS
SITEFINITY_SITE_PREFIX="https://your-sitefinity-site.com" python simple_server.py
```

## Environment Variables in Azure

When deploying to Azure App Service, set these environment variables in the application settings:

```
SITEFINITY_SITE_PREFIX=https://your-sitefinity-site.com
WEBSITES_PORT=8000
``` 