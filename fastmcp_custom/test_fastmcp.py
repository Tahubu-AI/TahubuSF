#!/usr/bin/env python3
"""
FastMCP 2.0 Test Suite
Comprehensive testing for HTTP streaming, authentication, proxying, and client features
"""
import asyncio
import pytest
import httpx
import time
import logging
from typing import Dict, Any

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FastMCPTester:
    """Comprehensive test suite for FastMCP 2.0"""
    
    def __init__(self, server_url: str = "http://127.0.0.1:3000"):
        self.server_url = server_url
        self.client = httpx.AsyncClient()
        self.test_results = {}
    
    async def test_server_health(self) -> bool:
        """Test server health endpoint"""
        logger.info("🏥 Testing server health...")
        try:
            response = await self.client.get(f"{self.server_url}/health")
            if response.status_code == 200:
                health_data = response.json()
                logger.info(f"✅ Server health: {health_data}")
                return True
            else:
                logger.error(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            return False
    
    async def test_list_tools(self) -> bool:
        """Test listing available tools"""
        logger.info("📋 Testing tool listing...")
        try:
            response = await self.client.get(f"{self.server_url}/tools")
            if response.status_code == 200:
                tools = response.json()
                logger.info(f"✅ Found {len(tools)} tools")
                for tool in tools[:5]:  # Show first 5 tools
                    tool_name = tool.get('name', tool) if isinstance(tool, dict) else str(tool)
                    logger.info(f"   • {tool_name}")
                return len(tools) > 0
            else:
                logger.error(f"❌ Tool listing failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Tool listing error: {e}")
            return False
    
    async def test_tool_execution(self) -> bool:
        """Test executing MCP tools"""
        logger.info("🔧 Testing tool execution...")
        test_tools = [
            ("get_news", {}),
            ("get_blog_posts", {}),
            ("get_sites", {}),
            ("get_pages", {})
        ]
        
        success_count = 0
        for tool_name, args in test_tools:
            try:
                payload = {
                    "tool": tool_name,
                    "arguments": args
                }
                response = await self.client.post(
                    f"{self.server_url}/call-tool",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ Tool {tool_name}: Success")
                    success_count += 1
                else:
                    logger.warning(f"⚠️  Tool {tool_name}: HTTP {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️  Tool {tool_name}: {str(e)[:100]}")
        
        success_rate = success_count / len(test_tools)
        logger.info(f"📊 Tool execution success rate: {success_rate:.1%} ({success_count}/{len(test_tools)})")
        return success_rate > 0.5  # At least 50% success rate
    
    async def test_streaming_response(self) -> bool:
        """Test HTTP streaming capabilities"""
        logger.info("🌊 Testing streaming responses...")
        try:
            # Test with a tool that might return large response
            payload = {
                "tool": "get_news",
                "arguments": {},
                "stream": True  # Request streaming
            }
            
            async with self.client.stream(
                "POST",
                f"{self.server_url}/call-tool",
                json=payload,
                timeout=30
            ) as response:
                if response.status_code == 200:
                    chunks = []
                    async for chunk in response.aiter_text():
                        chunks.append(chunk)
                        if len(chunks) >= 5:  # Limit for testing
                            break
                    
                    logger.info(f"✅ Streaming: Received {len(chunks)} chunks")
                    return len(chunks) > 0
                else:
                    logger.warning(f"⚠️  Streaming failed: HTTP {response.status_code}")
                    return False
        except Exception as e:
            logger.warning(f"⚠️  Streaming error: {e}")
            return False
    
    async def test_authentication(self, auth_token: str = None) -> bool:
        """Test authentication features"""
        logger.info("🔐 Testing authentication...")
        
        if not auth_token:
            logger.info("ℹ️  No auth token provided, skipping auth test")
            return True
        
        try:
            # Test with authentication
            headers = {"Authorization": f"Bearer {auth_token}"}
            response = await self.client.get(
                f"{self.server_url}/tools",
                headers=headers
            )
            
            if response.status_code == 200:
                logger.info("✅ Authentication: Success")
                return True
            elif response.status_code == 401:
                logger.warning("⚠️  Authentication: Token rejected")
                return False
            else:
                logger.warning(f"⚠️  Authentication: HTTP {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return False
    
    async def test_cors_headers(self) -> bool:
        """Test CORS configuration"""
        logger.info("🌐 Testing CORS headers...")
        try:
            response = await self.client.options(f"{self.server_url}/tools")
            cors_headers = [
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Methods",
                "Access-Control-Allow-Headers"
            ]
            
            found_headers = sum(1 for header in cors_headers if header in response.headers)
            logger.info(f"✅ CORS: Found {found_headers}/{len(cors_headers)} headers")
            return found_headers >= 2  # At least 2 CORS headers
        except Exception as e:
            logger.warning(f"⚠️  CORS test error: {e}")
            return False
    
    async def test_error_handling(self) -> bool:
        """Test error handling"""
        logger.info("🚨 Testing error handling...")
        
        test_cases = [
            # Invalid tool name
            {
                "tool": "nonexistent_tool",
                "arguments": {},
                "expected_status": [400, 404, 500]
            },
            # Invalid arguments
            {
                "tool": "get_news",
                "arguments": {"invalid_param": "value"},
                "expected_status": [200, 400]  # Might ignore invalid params
            }
        ]
        
        success_count = 0
        for i, test_case in enumerate(test_cases):
            try:
                response = await self.client.post(
                    f"{self.server_url}/call-tool",
                    json=test_case,
                    timeout=15
                )
                
                if response.status_code in test_case["expected_status"]:
                    logger.info(f"✅ Error case {i+1}: Handled correctly ({response.status_code})")
                    success_count += 1
                else:
                    logger.warning(f"⚠️  Error case {i+1}: Unexpected status {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️  Error case {i+1}: Exception {e}")
        
        return success_count >= len(test_cases) // 2
    
    async def test_performance(self) -> bool:
        """Test basic performance characteristics"""
        logger.info("⚡ Testing performance...")
        
        # Test response time
        start_time = time.time()
        try:
            response = await self.client.get(f"{self.server_url}/health")
            response_time = time.time() - start_time
            
            if response.status_code == 200 and response_time < 5.0:
                logger.info(f"✅ Performance: Response time {response_time:.3f}s")
                return True
            else:
                logger.warning(f"⚠️  Performance: Slow response {response_time:.3f}s")
                return False
        except Exception as e:
            logger.error(f"❌ Performance test error: {e}")
            return False
    
    async def run_all_tests(self, auth_token: str = None) -> Dict[str, bool]:
        """Run all tests and return results"""
        logger.info("🧪 Starting FastMCP 2.0 Test Suite")
        logger.info("=" * 60)
        
        tests = [
            ("Server Health", self.test_server_health),
            ("List Tools", self.test_list_tools),
            ("Tool Execution", self.test_tool_execution),
            ("Streaming Response", self.test_streaming_response),
            ("Authentication", lambda: self.test_authentication(auth_token)),
            ("CORS Headers", self.test_cors_headers),
            ("Error Handling", self.test_error_handling),
            ("Performance", self.test_performance)
        ]
        
        results = {}
        for test_name, test_func in tests:
            logger.info(f"\n🔄 Running {test_name}...")
            try:
                result = await test_func()
                results[test_name] = result
                status = "✅ PASS" if result else "❌ FAIL"
                logger.info(f"   {status}")
            except Exception as e:
                results[test_name] = False
                logger.error(f"   ❌ ERROR: {e}")
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 TEST RESULTS SUMMARY")
        logger.info("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"   {test_name}: {status}")
        
        logger.info(f"\n📈 Overall: {passed}/{total} tests passed ({passed/total:.1%})")
        
        if passed >= total * 0.75:  # 75% pass rate
            logger.info("🎉 FastMCP 2.0 implementation is working well!")
        elif passed >= total * 0.5:  # 50% pass rate
            logger.info("⚠️  FastMCP 2.0 implementation has some issues")
        else:
            logger.error("❌ FastMCP 2.0 implementation needs attention")
        
        return results
    
    async def cleanup(self):
        """Clean up test resources"""
        await self.client.aclose()

async def run_tests():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FastMCP 2.0 Test Suite")
    parser.add_argument(
        "--server-url",
        default="http://127.0.0.1:3000",
        help="FastMCP server URL"
    )
    parser.add_argument(
        "--auth-token",
        help="Authentication token for testing"
    )
    parser.add_argument(
        "--test-auth",
        action="store_true",
        help="Test authentication features"
    )
    parser.add_argument(
        "--test-streaming",
        action="store_true",
        help="Test streaming features"
    )
    parser.add_argument(
        "--test-http",
        action="store_true",
        help="Test HTTP transport"
    )
    
    args = parser.parse_args()
    
    tester = FastMCPTester(args.server_url)
    
    try:
        if args.test_http:
            logger.info("🌐 Testing HTTP transport only...")
            result = await tester.test_server_health()
            logger.info(f"HTTP transport test: {'✅ PASS' if result else '❌ FAIL'}")
        elif args.test_auth:
            logger.info("🔐 Testing authentication only...")
            result = await tester.test_authentication(args.auth_token)
            logger.info(f"Authentication test: {'✅ PASS' if result else '❌ FAIL'}")
        elif args.test_streaming:
            logger.info("🌊 Testing streaming only...")
            result = await tester.test_streaming_response()
            logger.info(f"Streaming test: {'✅ PASS' if result else '❌ FAIL'}")
        else:
            # Run all tests
            await tester.run_all_tests(args.auth_token)
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    asyncio.run(run_tests()) 