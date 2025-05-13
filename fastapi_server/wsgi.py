"""
WSGI entry point for gunicorn in production deployments
"""
from fastapi_server.main import app

# This file is used by gunicorn to run the app in production
# Command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker fastapi_server.wsgi:app 