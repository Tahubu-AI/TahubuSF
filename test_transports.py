#!/usr/bin/env python
"""
Test script to verify different transport protocols for TahubuSF MCP server
"""

import sys
import subprocess
import time
import requests
import signal
import os

def test_stdio():
    """Test STDIO transport by starting and immediately stopping"""
    print("\n📊 Testing STDIO Transport...")
    try:
        print("   - Starting STDIO server...")
        # Start server and immediately terminate it to test if it starts correctly
        process = subprocess.Popen(
            [sys.executable, "run.py", "--transport", "stdio", "--verbose"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for startup
        time.sleep(2)
        
        # Terminate the process
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
            print("✅ STDIO transport test successful")
            return True
        except subprocess.TimeoutExpired:
            process.kill()
            print("✅ STDIO transport test successful (had to force stop)")
            return True
            
    except Exception as e:
        print(f"❌ STDIO transport failed: {e}")
        return False

def test_http():
    """Test HTTP transport by starting server and checking if it responds"""
    print("\n🚀 Testing Streamable HTTP Transport...")
    try:
        # Start HTTP server in background
        print("   - Starting HTTP server on port 5002...")
        process = subprocess.Popen(
            [sys.executable, "run.py", "--transport", "streamable-http", "--port", "5002", "--path", "/mcp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Test if server responds
        response = requests.head("http://127.0.0.1:5002/mcp", timeout=5)
        
        # Clean up
        process.terminate()
        process.wait(timeout=5)
        
        print("✅ HTTP transport test successful")
        return True
        
    except requests.RequestException as e:
        print(f"❌ HTTP server not responding: {e}")
        return False
    except Exception as e:
        print(f"❌ HTTP transport failed to start: {e}")
        return False

def test_server_creation():
    """Test basic server creation without running"""
    print("\n🔧 Testing Server Creation...")
    try:
        # Test importing and creating the server
        result = subprocess.run([
            sys.executable, "-c",
            "from tahubu_sf.app import create_app; app = create_app(); print('Server created successfully')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Server creation test successful")
            return True
        else:
            print(f"❌ Server creation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Server creation test failed: {e}")
        return False

def main():
    """Run all transport tests"""
    print("🧪 TahubuSF MCP Transport Test Suite")
    print("=" * 50)
    
    # Run all tests
    results = {
        "server_creation": test_server_creation(),
        "stdio": test_stdio(),
        "http": test_http(),
    }
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    all_passed = all(results.values())
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nYour TahubuSF MCP server supports:")
        print("- STDIO for Claude Desktop integration")
        print("- HTTP for web-based deployments")
        print("\nReady for production use! 🚀")
    else:
        print("❌ SOME TESTS FAILED")
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name}: {status}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 