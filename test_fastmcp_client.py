#!/usr/bin/env python3
"""
Simple test script to verify FastMCP 2.0 client works with server
"""
import asyncio
import sys

async def test_fastmcp_client():
    """Test the FastMCP 2.0 client"""
    print("🧪 Testing FastMCP 2.0 Client Connection")
    print("=" * 50)
    
    try:
        from fastmcp import Client
        
        # Connect to the FastMCP server
        # Note: Server should be running on http://127.0.0.1:3000/mcp
        client = Client("http://127.0.0.1:3000/mcp")
        
        async with client:
            print("✅ Connected to FastMCP server")
            
            # List available tools
            print("\n📋 Listing tools...")
            tools = await client.list_tools()
            print(f"✅ Found {len(tools)} tools")
            
            # Show first few tools
            print("   Available tools:")
            for i, tool in enumerate(tools[:5]):
                print(f"   • {tool.name}")
            if len(tools) > 5:
                print(f"   ... and {len(tools) - 5} more")
            
            # Test a simple tool
            print("\n🧪 Testing get_sites tool...")
            try:
                result = await client.call_tool("get_sites")
                # Extract content from MCP response
                if hasattr(result, '__iter__') and len(result) > 0:
                    content = result[0].text if hasattr(result[0], 'text') else str(result[0])
                else:
                    content = str(result)
                
                print(f"✅ get_sites completed successfully!")
                print(f"📄 Full result ({len(content)} characters):")
                print("-" * 40)
                print(content)
                print("-" * 40)
                
            except Exception as e:
                print(f"❌ get_sites failed: {e}")
            
            # Test another tool for comparison
            print("\n🧪 Testing get_blog_posts tool...")
            try:
                result = await client.call_tool("get_blog_posts")
                # Extract content from MCP response
                if hasattr(result, '__iter__') and len(result) > 0:
                    content = result[0].text if hasattr(result[0], 'text') else str(result[0])
                else:
                    content = str(result)
                
                print(f"✅ get_blog_posts completed successfully!")
                print(f"📄 Full result ({len(content)} characters):")
                print("-" * 40)
                # Show first 500 characters for blog posts (might be long)
                if len(content) > 500:
                    print(content[:500] + "...")
                    print(f"[Truncated - showing first 500 of {len(content)} characters]")
                else:
                    print(content)
                print("-" * 40)
                
            except Exception as e:
                print(f"❌ get_blog_posts failed: {e}")
            
            print("\n🎉 FastMCP client test completed!")
            return True
            
    except ImportError:
        print("❌ FastMCP library not available")
        print("   Make sure FastMCP is installed: pip install fastmcp")
        return False
    except Exception as e:
        print(f"❌ Client test failed: {e}")
        return False

if __name__ == "__main__":
    print("Make sure the FastMCP server is running:")
    print("  python fastmcp_custom/server.py --transport streamable-http --port 3000")
    print("  or")
    print("  python run_fastmcp.py (select option 1)")
    print()
    
    try:
        success = asyncio.run(test_fastmcp_client())
        if success:
            print("\n✅ FastMCP client is working correctly!")
        else:
            print("\n❌ FastMCP client test failed")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1) 