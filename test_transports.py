#!/usr/bin/env python
"""
Test script to verify different transport protocols work correctly
"""
import subprocess
import sys
import time
import json
import requests
from pathlib import Path

def test_stdio():
    """Test STDIO transport by checking if the server can be imported and run"""
    print("🔌 Testing STDIO Transport...")
    try:
        # Import the app to verify it works
        from tahubu_sf.app import create_app
        app = create_app()
        print("✅ STDIO transport setup successful")
        print(f"   - Server created with FastMCP")
        
        # Test that the server has tools
        tools = getattr(app, '_tools', {})
        print(f"   - {len(tools)} tools registered")
        return True
    except Exception as e:
        print(f"❌ STDIO transport failed: {e}")
        return False

def test_sse():
    """Test SSE transport by starting server and checking if it responds"""
    print("\n🌐 Testing SSE Transport...")
    
    # Start SSE server in background
    process = None
    try:
        process = subprocess.Popen(
            [sys.executable, "run.py", "--transport", "sse", "--port", "5001"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        print("   - Starting SSE server on port 5001...")
        time.sleep(3)
        
        # Check if server is responding
        try:
            response = requests.get("http://127.0.0.1:5001/sse", timeout=5)
            print(f"   - Server responding (Status: {response.status_code})")
            print("✅ SSE transport test successful")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ SSE server not responding: {e}")
            return False
    except Exception as e:
        print(f"❌ SSE transport failed to start: {e}")
        return False
    finally:
        if process:
            process.terminate()
            process.wait()

def test_http():
    """Test Streamable HTTP transport"""
    print("\n🚀 Testing Streamable HTTP Transport...")
    
    # Start HTTP server in background
    process = None
    try:
        process = subprocess.Popen(
            [sys.executable, "run.py", "--transport", "streamable-http", "--port", "5002", "--path", "/mcp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        print("   - Starting HTTP server on port 5002...")
        time.sleep(3)
        
        # Check if server is responding
        try:
            response = requests.get("http://127.0.0.1:5002/mcp", timeout=5)
            print(f"   - Server responding (Status: {response.status_code})")
            print("✅ HTTP transport test successful")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ HTTP server not responding: {e}")
            return False
    except Exception as e:
        print(f"❌ HTTP transport failed to start: {e}")
        return False
    finally:
        if process:
            process.terminate()
            process.wait()

def main():
    """Run all transport tests"""
    print("🧪 TahubuSF Transport Protocol Tests")
    print("=" * 50)
    
    results = {
        "stdio": test_stdio(),
        "sse": test_sse(),
        "http": test_http()
    }
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    for transport, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{transport.upper():12} {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All transport protocols are working correctly!")
        print("\nYou can now use:")
        print("- STDIO for Claude Desktop integration")
        print("- SSE for web-based MCP clients") 
        print("- HTTP for modern web deployments")
    else:
        print("\n⚠️  Some transport protocols have issues.")
        print("Please check the error messages above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 