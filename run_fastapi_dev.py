#!/usr/bin/env python
"""
Simple direct test script for the FastAPI server
This script avoids complex imports and just runs the server directly
"""
import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# Base directory is the project root
BASE_DIR = Path(__file__).resolve().parent
print(f"Project root directory: {BASE_DIR}")

# Install required packages if needed
try:
    import fastapi
    import uvicorn
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn[standard]"])
    
# Create a temporary script to run the server
temp_script = os.path.join(BASE_DIR, "temp_server.py")
with open(temp_script, "w") as f:
    f.write("""
import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = str(Path(__file__).resolve().parent)
sys.path.insert(0, project_root)

# Import the FastAPI app
try:
    from fastapi_server.main import app
    import uvicorn
    
    # Port to run the server on
    port = 8000
    
    # Start the server
    print(f"Starting server on http://localhost:{port}")
    uvicorn.run(app, host="localhost", port=port)
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
""")

try:
    # Open the browser
    url = "http://localhost:8000/inspector/"
    print(f"Starting server on http://localhost:8000")
    print(f"Opening browser to {url}")
    webbrowser.open(url)
    
    # Run the server
    print("Running server...")
    result = subprocess.run([sys.executable, temp_script], check=True)
    print(f"Server exited with code {result.returncode}")
    
except KeyboardInterrupt:
    print("Interrupted by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up the temporary file
    if os.path.exists(temp_script):
        os.remove(temp_script)
        print("Temporary files cleaned up") 