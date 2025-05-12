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

import requests

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent

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

if __name__ == "__main__":
    main() 