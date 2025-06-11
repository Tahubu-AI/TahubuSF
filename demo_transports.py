#!/usr/bin/env python
"""
Interactive demo of TahubuSF MCP server transport protocols
"""

import subprocess
import sys
import time

def demo_stdio():
    """Demo STDIO transport"""
    print("\n📊 STDIO Transport Demo")
    print("=" * 40)
    print("This transport is perfect for Claude Desktop integration.")
    print("\nClaude Desktop Configuration:")
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
}""")
    
    response = input("\nWould you like to test the STDIO server? (y/n): ")
    if response.lower() == 'y':
        print("Starting STDIO server... (Press Ctrl+C to stop)")
        try:
            subprocess.run(["python", "run.py", "--transport", "stdio", "--verbose"], check=True)
        except KeyboardInterrupt:
            print("\nSTDIO server stopped.")
        except subprocess.CalledProcessError as e:
            print(f"Error starting STDIO server: {e}")

def demo_http():
    """Demo HTTP transport"""
    print("\n🚀 Streamable HTTP Transport Demo")
    print("=" * 40)
    print("This transport is perfect for web deployments and production use.")
    print("\nStarting HTTP server on http://127.0.0.1:5000/mcp")
    print("\nClaude Desktop Configuration:")
    print("""
{
    "mcpServers":{
        "TahubuSF-HTTP": {
            "url": "http://127.0.0.1:5000/mcp"
        }
    }
}""")
    
    response = input("\nWould you like to start the HTTP server? (y/n): ")
    if response.lower() == 'y':
        print("Starting HTTP server... (Press Ctrl+C to stop)")
        try:
            subprocess.run(["python", "run.py", "--transport", "streamable-http", "--port", "5000", "--path", "/mcp"], check=True)
        except KeyboardInterrupt:
            print("\nHTTP server stopped.")
        except subprocess.CalledProcessError as e:
            print(f"Error starting HTTP server: {e}")

def main():
    """Main demo menu"""
    print("🎭 TahubuSF MCP Transport Demo")
    print("=" * 50)
    print("\nAvailable transport protocols:")
    print("1. 📊 STDIO Transport (Command-based)")
    print("2. 🚀 HTTP Transport (Web-based)")
    print("3. 🚪 Exit")
    
    while True:
        try:
            choice = input("\nSelect a transport to demo (1-3): ").strip()
            
            if choice == '1':
                demo_stdio()
            elif choice == '2':
                demo_http()
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 