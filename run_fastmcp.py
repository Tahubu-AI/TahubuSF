#!/usr/bin/env python3
"""
Quick Start Script for FastMCP 2.0
Convenient way to launch the FastMCP 2.0 server with different configurations
"""
import subprocess
import sys
import argparse
import time
import webbrowser
from pathlib import Path

def run_basic_server():
    """Start basic FastMCP 2.0 HTTP server"""
    print("🚀 Starting FastMCP 2.0 Basic HTTP Server...")
    print("   URL: http://127.0.0.1:3000")
    print("   Features: Streamable HTTP transport, All MCP tools")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    subprocess.run([
        sys.executable, "fastmcp_custom/server.py",
        "--transport", "streamable-http",
        "--port", "3000",
        "--verbose"
    ])

def run_authenticated_server():
    """Start FastMCP 2.0 server with authentication"""
    print("🔐 Starting FastMCP 2.0 Authenticated Server...")
    print("   URL: http://127.0.0.1:3000")
    print("   Features: Streamable HTTP transport, Authentication, All MCP tools")
    print("   Auth Token: demo-token-12345")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    subprocess.run([
        sys.executable, "fastmcp_custom/server.py",
        "--transport", "streamable-http",
        "--port", "3000",
        "--auth",
        "--auth-token", "demo-token-12345",
        "--verbose"
    ])

def run_production_server():
    """Start FastMCP 2.0 server in production mode"""
    print("🌐 Starting FastMCP 2.0 Production Server...")
    print("   URL: http://0.0.0.0:3000")
    print("   Features: Streamable HTTP transport, Authentication, CORS, All MCP tools")
    print("   Auth Token: production-token-67890")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    subprocess.run([
        sys.executable, "fastmcp_custom/server.py",
        "--transport", "streamable-http",
        "--host", "0.0.0.0",
        "--port", "3000",
        "--auth",
        "--auth-token", "production-token-67890"
    ])

def run_stdio_server():
    """Start FastMCP 2.0 server with STDIO transport (Claude Desktop)"""
    print("📊 Starting FastMCP 2.0 STDIO Server...")
    print("   Transport: STDIO (for Claude Desktop)")
    print("   Features: All MCP tools, Claude Desktop compatible")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    subprocess.run([
        sys.executable, "fastmcp_custom/server.py",
        "--transport", "stdio",
        "--verbose"
    ])

def run_sse_server():
    """Start FastMCP 2.0 server with SSE transport"""
    print("📡 Starting FastMCP 2.0 SSE Server...")
    print("   URL: http://127.0.0.1:3000")
    print("   Features: SSE transport, All MCP tools")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    subprocess.run([
        sys.executable, "fastmcp_custom/server.py",
        "--transport", "sse",
        "--port", "3000",
        "--verbose"
    ])

def test_client():
    """Test the FastMCP 2.0 client"""
    print("🧪 Testing FastMCP 2.0 Client...")
    print("   Connecting to: http://127.0.0.1:3000/mcp")
    print("   Features: Client library, Tool testing")
    print("-" * 50)
    
    subprocess.run([
        sys.executable, "test_fastmcp_client.py"
    ])

def run_comprehensive_tests():
    """Run comprehensive test suite"""
    print("🧪 Running FastMCP 2.0 Test Suite...")
    print("   Target: http://127.0.0.1:3000")
    print("   Features: All features, All tools")
    print("-" * 50)
    
    subprocess.run([
        sys.executable, "fastmcp_custom/test_fastmcp.py",
        "--server-url", "http://127.0.0.1:3000"
    ])

def show_info():
    """Show FastMCP 2.0 information"""
    print("📋 FastMCP 2.0 Information")
    print("=" * 50)
    
    # Show package info
    print("\nFastMCP 2.0 Features:")
    print("✅ Streamable HTTP Transport")
    print("✅ SSE (Server-Sent Events) Transport")
    print("✅ STDIO Transport (Claude Desktop)")
    print("✅ Authentication & Security") 
    print("✅ Remote Server Proxying")
    print("✅ Client Library")
    print("✅ Production Ready")
    
    # Show available transports
    print("\nSupported Transports:")
    print("🌐 streamable-http → Modern HTTP streaming (Recommended)")
    print("📡 sse            → Server-Sent Events (Legacy)")
    print("📊 stdio          → Standard I/O (Claude Desktop)")

def show_architecture():
    """Show the complete architecture"""
    print("🏗️  TahubuSF Architecture Overview")
    print("=" * 50)
    print()
    print("Current Architecture (All Working):")
    print("├── tahubu_sf/           # 28 MCP Tools (Core)")
    print("├── run.py               # STDIO Transport (Claude Desktop)")
    print("├── fastapi_server/      # Traditional REST API")
    print("└── fastmcp_custom/      # 🆕 FastMCP 2.0 (New)")
    print("    ├── server.py        #     HTTP Streaming Server")
    print("    ├── client.py        #     Client Library")
    print("    ├── config.py        #     Configuration")
    print("    └── test_fastmcp.py  #     Test Suite")
    print()
    print("Transport Options:")
    print("📊 STDIO           → Claude Desktop (use run.py)")
    print("🌐 REST/HTTP       → Web/Production (use fastapi_server/)")
    print("🚀 Streamable HTTP → Advanced HTTP (use fastmcp_custom/)")
    print("📡 SSE             → Server-Sent Events (use fastmcp_custom/)")
    print()
    print("FastMCP 2.0 Advantages:")
    print("✅ Multiple HTTP transports")
    print("✅ Streaming capabilities")
    print("✅ Authentication")
    print("✅ Remote Proxying")
    print("✅ Client Library")
    print("✅ Production Features")

def main():
    """Main menu"""
    parser = argparse.ArgumentParser(description="FastMCP 2.0 Quick Start")
    parser.add_argument("--info", action="store_true", help="Show FastMCP 2.0 information")
    parser.add_argument("--architecture", action="store_true", help="Show architecture overview")
    
    args = parser.parse_args()
    
    if args.info:
        show_info()
        return
    
    if args.architecture:
        show_architecture()
        return
    
    print("🚀 FastMCP 2.0 Quick Start Menu")
    print("=" * 50)
    print("Choose your deployment option:")
    print()
    print("1. 🌐 Basic Streamable HTTP Server (port 3000)")
    print("2. 🔐 Authenticated Server (with demo token)")
    print("3. 🏭 Production Server (0.0.0.0:3000)")
    print("4. 📊 STDIO Server (Claude Desktop)")
    print("5. 📡 SSE Server (Server-Sent Events)")
    print("6. 🧪 Test Client")
    print("7. 🧪 Run Test Suite")
    print("8. 📋 Show Info")
    print("9. 🏗️  Show Architecture")
    print("10. 🚪 Exit")
    print()
    
    while True:
        try:
            choice = input("Select option (1-10): ").strip()
            
            if choice == "1":
                run_basic_server()
            elif choice == "2":
                run_authenticated_server()
            elif choice == "3":
                run_production_server()
            elif choice == "4":
                run_stdio_server()
            elif choice == "5":
                run_sse_server()
            elif choice == "6":
                test_client()
            elif choice == "7":
                run_comprehensive_tests()
            elif choice == "8":
                show_info()
            elif choice == "9":
                show_architecture()
            elif choice == "10":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-10.")
            
            print("\n" + "=" * 50)
            print("Select another option or 10 to exit:")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 