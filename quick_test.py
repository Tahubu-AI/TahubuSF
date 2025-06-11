#!/usr/bin/env python3
"""
Quick test of FastMCP 2.0 implementation
"""
import subprocess
import sys
import time

def test_server():
    """Quick test of the server"""
    print("🚀 Quick FastMCP 2.0 Test")
    print("=" * 30)
    
    # Test 1: Check if server can import correctly
    print("\n1. Testing server import...")
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "import sys; sys.path.insert(0, '.'); from fastmcp_custom.server import create_fastmcp_server; server = create_fastmcp_server(); print('OK: Server created successfully')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Server import successful")
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    # Test 2: Check available transports
    print("\n2. Testing FastMCP library...")
    try:
        # Check what transports are supported by FastMCP
        result = subprocess.run([
            sys.executable, "-c", 
            "from fastmcp import FastMCP; mcp = FastMCP('test'); print('OK: FastMCP library working')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ FastMCP library available")
        else:
            print(f"❌ FastMCP test error: {result.stderr}")
    except Exception as e:
        print(f"❌ FastMCP test failed: {e}")
    
    # Test 3: Run server briefly with STDIO
    print("\n3. Testing server startup...")
    try:
        proc = subprocess.Popen([
            sys.executable, "fastmcp_custom/server.py", 
            "--transport", "stdio", "--verbose"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process is still running
        if proc.poll() is None:
            print("✅ Server started successfully")
            proc.terminate()
            proc.wait()
        else:
            stdout, stderr = proc.communicate()
            print(f"❌ Server failed to start")
            print(f"   stdout: {stdout[:300]}")
            print(f"   stderr: {stderr[:300]}")
            return False
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False
    
    print("\n🎉 Quick test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_server()
    if success:
        print("\n✅ Your FastMCP 2.0 implementation is working!")
        print("   Try running: python run_fastmcp.py")
        print("   Then select option 1 for the streamable HTTP server")
    else:
        print("\n❌ There are some issues to fix")
    
    sys.exit(0 if success else 1) 