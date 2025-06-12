#!/usr/bin/env python3
"""
FastMCP 2.0 Simple Test Suite
Tests FastMCP server functionality without external dependencies
"""
import asyncio
import sys
import logging
import argparse
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FastMCPSimpleTester:
    """Simple test suite for FastMCP 2.0"""
    
    def __init__(self, server_url: str = "http://127.0.0.1:3000/mcp"):
        self.server_url = server_url
        self.test_results = {}
    
    async def test_fastmcp_client_connection(self) -> bool:
        """Test FastMCP client connection and basic functionality"""
        logger.info("🧪 Testing FastMCP Client Connection")
        
        try:
            from fastmcp import Client
            
            # Connect to the FastMCP server
            client = Client(self.server_url)
            
            async with client:
                logger.info("✅ Connected to FastMCP server")
                
                # List available tools
                logger.info("📋 Listing tools...")
                tools = await client.list_tools()
                logger.info(f"✅ Found {len(tools)} tools")
                
                if len(tools) == 0:
                    logger.error("❌ No tools found!")
                    return False
                
                # Show first few tools
                logger.info("   Available tools:")
                for i, tool in enumerate(tools[:5]):
                    logger.info(f"   • {tool.name}")
                if len(tools) > 5:
                    logger.info(f"   ... and {len(tools) - 5} more")
                
                return True
                
        except ImportError:
            logger.error("❌ FastMCP library not available")
            logger.error("   Make sure FastMCP is installed: pip install fastmcp")
            return False
        except Exception as e:
            logger.error(f"❌ Client connection test failed: {e}")
            return False
    
    async def test_tool_execution(self) -> bool:
        """Test executing some basic tools"""
        logger.info("🔧 Testing tool execution...")
        
        try:
            from fastmcp import Client
            
            client = Client(self.server_url)
            
            async with client:
                # Test simple tools that should exist
                test_tools = [
                    "get_sites",
                    "get_news", 
                    "get_blog_posts"
                ]
                
                success_count = 0
                for tool_name in test_tools:
                    try:
                        logger.info(f"🧪 Testing {tool_name}...")
                        result = await client.call_tool(tool_name)
                        
                        # Extract content from MCP response
                        if hasattr(result, '__iter__') and len(result) > 0:
                            content = result[0].text if hasattr(result[0], 'text') else str(result[0])
                        else:
                            content = str(result)
                        
                        logger.info(f"✅ {tool_name} completed ({len(content)} characters)")
                        success_count += 1
                        
                    except Exception as e:
                        logger.warning(f"⚠️  {tool_name} failed: {e}")
                
                success_rate = success_count / len(test_tools)
                logger.info(f"📊 Tool execution success rate: {success_rate:.1%} ({success_count}/{len(test_tools)})")
                return success_rate > 0.5  # At least 50% success
                
        except Exception as e:
            logger.error(f"❌ Tool execution test failed: {e}")
            return False
    
    async def test_server_responsiveness(self) -> bool:
        """Test server response times"""
        logger.info("⏱️  Testing server responsiveness...")
        
        try:
            from fastmcp import Client
            import time
            
            client = Client(self.server_url)
            
            async with client:
                # Test multiple quick requests
                start_time = time.time()
                
                for i in range(3):
                    await client.list_tools()
                
                end_time = time.time()
                avg_time = (end_time - start_time) / 3
                
                logger.info(f"✅ Average response time: {avg_time:.2f}s")
                return avg_time < 5.0  # Should respond within 5 seconds
                
        except Exception as e:
            logger.error(f"❌ Responsiveness test failed: {e}")
            return False
    
    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests and return results"""
        logger.info("🚀 Starting FastMCP 2.0 Test Suite")
        logger.info("=" * 50)
        
        tests = [
            ("Connection", self.test_fastmcp_client_connection),
            ("Tool Execution", self.test_tool_execution),
            ("Responsiveness", self.test_server_responsiveness)
        ]
        
        results = {}
        passed = 0
        
        for test_name, test_func in tests:
            logger.info(f"\n🧪 Running test: {test_name}")
            try:
                result = await test_func()
                results[test_name] = result
                if result:
                    passed += 1
                    logger.info(f"✅ {test_name}: PASSED")
                else:
                    logger.error(f"❌ {test_name}: FAILED")
            except Exception as e:
                results[test_name] = False
                logger.error(f"❌ {test_name}: ERROR - {e}")
        
        # Summary
        logger.info("\n" + "=" * 50)
        logger.info(f"🎯 Test Results: {passed}/{len(tests)} passed")
        
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"   {test_name}: {status}")
        
        if passed == len(tests):
            logger.info("🎉 All tests passed! FastMCP 2.0 is working correctly!")
        else:
            logger.warning(f"⚠️  {len(tests) - passed} test(s) failed. Check server and configuration.")
        
        return results

async def main():
    """Main test execution"""
    parser = argparse.ArgumentParser(description="FastMCP 2.0 Simple Test Suite")
    parser.add_argument(
        "--server-url", 
        default="http://127.0.0.1:3000",
        help="FastMCP server URL (without /mcp suffix)"
    )
    
    args = parser.parse_args()
    
    print("FastMCP 2.0 Simple Test Suite")
    print("=" * 40)
    print("Make sure the FastMCP server is running:")
    print("  python fastmcp_custom/server.py --transport streamable-http --port 3000")
    print()
    
    # Ensure the URL has /mcp suffix for FastMCP client
    server_url = args.server_url
    if not server_url.endswith('/mcp'):
        server_url += '/mcp'
    
    print(f"Testing server at: {server_url}")
    print()
    
    tester = FastMCPSimpleTester(server_url)
    
    try:
        results = await tester.run_all_tests()
        
        # Exit with appropriate code
        all_passed = all(results.values())
        sys.exit(0 if all_passed else 1)
        
    except KeyboardInterrupt:
        logger.info("\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Test suite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 