#!/usr/bin/env python
"""
Test script to verify the TahubuSF FastAPI server works correctly.
This script starts the server, opens a browser, and runs test requests.
"""
import os
import sys
import time
import json
import logging
import webbrowser
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path

# First make sure we have the requests module
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("test_fastapi")

# Server settings
HOST = "localhost"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"

def start_server() -> subprocess.Popen:
    """Start the FastAPI server process"""
    logger.info(f"Starting FastAPI server on {HOST}:{PORT}")
    
    env = os.environ.copy()
    env["PORT"] = str(PORT)
    
    # Run the server using the fastapi_server/run.py script
    run_script = os.path.join(os.path.dirname(__file__), "run.py")
    
    try:
        # Try to directly import and run the module
        logger.info("Attempting to directly start the server...")
        
        # Create a temporary module to run in a separate process
        temp_script = os.path.join(BASE_DIR, "temp_fastapi.py")
        with open(temp_script, "w") as f:
            f.write("""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi_server.main import app
import uvicorn
uvicorn.run(app, host="localhost", port=8000)
            """.strip())
        
        # Run the temporary module
        process = subprocess.Popen(
            [sys.executable, temp_script],
            env=env
        )
        
        return process
    except Exception as e:
        logger.error(f"Error starting server directly: {e}")
        logger.info("Falling back to subprocess method...")
        
        # Fall back to running the script directly
        process = subprocess.Popen(
            [sys.executable, run_script, "--port", str(PORT)],
            env=env
        )
        
        return process

def wait_for_server(max_retries: int = 10, retry_interval: float = 1.0) -> bool:
    """Wait for the server to be ready"""
    logger.info("Waiting for server to start...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                logger.info("Server is up and running!")
                return True
        except requests.ConnectionError:
            pass
        except Exception as e:
            logger.warning(f"Error while waiting for server: {str(e)}")
        
        logger.info(f"Waiting... ({i+1}/{max_retries})")
        time.sleep(retry_interval)
    
    logger.error("Server failed to start within the retry limit")
    return False

def run_api_tests() -> bool:
    """Run tests against the API endpoints"""
    logger.info("Running API tests...")
    all_passed = True
    
    # Test endpoints to check
    endpoints = [
        {
            "name": "Health Check",
            "url": "/health",
            "method": "GET",
            "expected_status": 200,
            "validator": lambda r: "status" in r.json() and r.json()["status"] == "healthy"
        },
        {
            "name": "List Tools",
            "url": "/api/list-tools",
            "method": "GET", 
            "expected_status": 200,
            "validator": lambda r: "tools" in r.json() and len(r.json()["tools"]) > 0
        },
        {
            "name": "Run Tool - News",
            "url": "/api/run-tool",
            "method": "POST",
            "data": {"name": "getNews", "params": {}},
            "expected_status": 200,
            "validator": lambda r: "result" in r.json() and len(r.json()["result"]) > 0
        }
    ]
    
    # Run tests
    for test in endpoints:
        logger.info(f"Testing: {test['name']}")
        
        try:
            if test["method"].upper() == "GET":
                response = requests.get(f"{BASE_URL}{test['url']}")
            elif test["method"].upper() == "POST":
                response = requests.post(
                    f"{BASE_URL}{test['url']}", 
                    json=test.get("data", {})
                )
            else:
                logger.error(f"Unsupported method: {test['method']}")
                all_passed = False
                continue
                
            # Check status code
            status_ok = response.status_code == test["expected_status"]
            if not status_ok:
                logger.error(f"  ❌ Status code: expected {test['expected_status']}, got {response.status_code}")
                all_passed = False
                continue
            
            # Run custom validator if provided
            validator = test.get("validator")
            if validator and not validator(response):
                logger.error(f"  ❌ Validation failed for {test['name']}")
                all_passed = False
                continue
                
            logger.info(f"  ✅ Test passed")
            
        except Exception as e:
            logger.error(f"  ❌ Error: {str(e)}")
            all_passed = False
    
    # Summary
    if all_passed:
        logger.info("✅ All tests passed successfully!")
    else:
        logger.error("❌ Some tests failed")
        
    return all_passed

def main():
    """Main function to run the test script"""
    logger.info("TahubuSF FastAPI Server Test")
    
    # Start the server
    server_process = start_server()
    
    try:
        # Wait for the server to start
        if wait_for_server():
            # Open browser
            logger.info(f"Opening browser to {BASE_URL}")
            webbrowser.open(BASE_URL)
            
            # Run API tests
            run_api_tests()
            
            # Keep server running
            logger.info("\nServer is running. Press Ctrl+C to stop...")
            while True:
                time.sleep(1)
                
    except KeyboardInterrupt:
        logger.info("\nStopping server...")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        # Terminate the server process
        if server_process:
            server_process.terminate()
            server_process.wait()
            logger.info("Server stopped")
            
            # Remove temporary file if it exists
            temp_script = os.path.join(BASE_DIR, "temp_fastapi.py")
            if os.path.exists(temp_script):
                try:
                    os.remove(temp_script)
                except Exception:
                    pass

if __name__ == "__main__":
    main() 