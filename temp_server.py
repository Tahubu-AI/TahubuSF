
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
