#!/usr/bin/env python
"""
Demo script to showcase different transport options for TahubuSF MCP server
"""
import subprocess
import time
import webbrowser
from pathlib import Path

def demo_stdio():
    """Demo STDIO transport"""
    print("🔌 STDIO Transport Demo")
    print("=" * 50)
    print("This is the default transport for Claude Desktop integration.")
    print("The server runs in stdio mode and communicates via stdin/stdout.")
    print("\nTo test with Claude Desktop, use this configuration:")
    print("""
{
    "mcpServers":{
        "TahubuSF": {
            "command": "uv",
            "args": [
                "--directory",
                "D:\\\\repos\\\\TahubuSF",
                "run",
                "run.py"
            ]
        }
    }
}
""")
    print("\nPress Enter to continue...")
    input()

def demo_sse():
    """Demo SSE transport"""
    print("\n🌐 SSE Transport Demo")
    print("=" * 50)
    print("Starting SSE server on http://127.0.0.1:5000/sse")
    print("This allows web-based MCP clients to connect via Server-Sent Events.")
    print("\nTo test with Claude Desktop, use this configuration:")
    print("""
{
    "mcpServers":{
        "TahubuSF-SSE": {
            "url": "http://127.0.0.1:5000/sse"
        }
    }
}
""")
    
    response = input("\nWould you like to start the SSE server? (y/n): ")
    if response.lower() == 'y':
        print("Starting SSE server... (Press Ctrl+C to stop)")
        try:
            subprocess.run(["python", "run.py", "--transport", "sse", "--port", "5000"], check=True)
        except KeyboardInterrupt:
            print("\nSSE server stopped.")
        except subprocess.CalledProcessError as e:
            print(f"Error starting SSE server: {e}")

def demo_http():
    """Demo Streamable HTTP transport"""
    print("\n🚀 Streamable HTTP Transport Demo")
    print("=" * 50)
    print("Starting HTTP server on http://127.0.0.1:5000/mcp")
    print("This is the modern HTTP transport recommended for web deployments.")
    print("\nTo test with Claude Desktop, use this configuration:")
    print("""
{
    "mcpServers":{
        "TahubuSF-HTTP": {
            "url": "http://127.0.0.1:5000/mcp"
        }
    }
}
""")
    
    response = input("\nWould you like to start the HTTP server? (y/n): ")
    if response.lower() == 'y':
        print("Starting HTTP server... (Press Ctrl+C to stop)")
        try:
            subprocess.run(["python", "run.py", "--transport", "streamable-http", "--port", "5000", "--path", "/mcp"], check=True)
        except KeyboardInterrupt:
            print("\nHTTP server stopped.")
        except subprocess.CalledProcessError as e:
            print(f"Error starting HTTP server: {e}")

def show_help():
    """Show help for the run.py command"""
    print("\n📚 Available Command Line Options")
    print("=" * 50)
    try:
        result = subprocess.run(["python", "run.py", "--help"], capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting help: {e}")

def main():
    """Main demo function"""
    print("🎯 TahubuSF MCP Server Transport Demo")
    print("=" * 60)
    print("This demo showcases the different transport protocols available")
    print("for the TahubuSF MCP server using FastMCP 2.0")
    print()
    
    while True:
        print("\nSelect a demo option:")
        print("1. 🔌 STDIO Transport (Claude Desktop)")
        print("2. 🌐 SSE Transport (Server-Sent Events)")
        print("3. 🚀 HTTP Transport (Modern Web)")
        print("4. 📚 Show Command Line Help")
        print("5. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            demo_stdio()
        elif choice == "2":
            demo_sse()
        elif choice == "3":
            demo_http()
        elif choice == "4":
            show_help()
        elif choice == "5":
            print("\n👋 Thanks for trying the TahubuSF MCP server!")
            break
        else:
            print("❌ Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main() 