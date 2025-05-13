#!/usr/bin/env python
"""
Wrapper script to run the FastAPI server from the project root
"""
import sys
import os
import importlib.util
from pathlib import Path

# Get the directory of this script and add to Python path
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir))

# Set PYTHONPATH for subprocess
os.environ["PYTHONPATH"] = str(script_dir)

if __name__ == "__main__":
    # Try direct method first
    try:
        # Import and run directly
        from fastapi_server.run import main
        main()
    except (ModuleNotFoundError, ImportError) as e:
        print(f"Error importing directly: {e}")
        print("Trying alternative method...")
        
        # Create a temporary module that handles its own imports
        temp_script = os.path.join(script_dir, "temp_run.py")
        try:
            with open(temp_script, "w") as f:
                f.write("""
import sys
import os
from pathlib import Path
# Add the project directory to the path
sys.path.insert(0, str(Path(__file__).resolve().parent))
# Import what we need
from fastapi_server.main import app
import uvicorn
# Get port from command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--host", type=str, default="0.0.0.0")
args = parser.parse_args()
# Run the app
print(f"Starting server on {args.host}:{args.port}")
uvicorn.run(app, host=args.host, port=args.port)
                """.strip())
            
            # Run the script with all the original arguments
            import subprocess
            subprocess.run([sys.executable, temp_script] + sys.argv[1:])
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_script):
                os.remove(temp_script) 