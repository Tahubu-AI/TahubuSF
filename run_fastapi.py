#!/usr/bin/env python
"""
Wrapper script to run the FastAPI server from the project root
"""
import sys
import os
from pathlib import Path

# Get the directory of this script
script_dir = Path(__file__).resolve().parent

# Add the project root to the Python path
sys.path.insert(0, str(script_dir))

# Import and run the fastapi_server script
from fastapi_server.run import main

if __name__ == "__main__":
    # Run the server
    main() 