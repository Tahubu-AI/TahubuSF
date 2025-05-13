#!/usr/bin/env python
"""
Wrapper script to run the FastAPI server tests from the project root
"""
import sys
import os
from pathlib import Path

# Get the directory of this script
script_dir = Path(__file__).resolve().parent

# Add the project root to the Python path
sys.path.insert(0, str(script_dir))

# Fix Python path for direct import
os.environ["PYTHONPATH"] = str(script_dir)

# Start the test directly to avoid import issues
if __name__ == "__main__":
    # Run the server test program directly
    server_process = None
    
    try:
        # Import and run directly
        from fastapi_server.test import main
        main()
    except ModuleNotFoundError as e:
        print(f"Error importing module: {e}")
        print("Trying alternative method...")
        
        # If import fails, run as subprocess with proper environment
        import subprocess
        
        server_process = subprocess.Popen(
            [sys.executable, "-m", "fastapi_server.test"],
            env={**os.environ, "PYTHONPATH": str(script_dir)}
        )
        
        # Wait for process to complete
        server_process.wait() 