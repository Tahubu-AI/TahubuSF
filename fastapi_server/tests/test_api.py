"""
Tests for the FastAPI server API
"""
import pytest
from fastapi.testclient import TestClient

from fastapi_server.main import app

# Create test client
client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_root_endpoint():
    """Test root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")

def test_list_tools_endpoint():
    """Test listing available tools"""
    response = client.get("/api/list-tools")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert isinstance(data["tools"], list)
    assert len(data["tools"]) > 0
    
    # Check structure of tool info
    tool = data["tools"][0]
    assert "name" in tool
    assert "description" in tool

def test_run_tool_endpoint_invalid_tool():
    """Test running non-existent tool"""
    response = client.post(
        "/api/run-tool",
        json={"name": "nonExistentTool", "params": {}}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Unknown tool" in data["detail"]

# Note: Additional tests for actually running tools would require mocking
# the underlying API calls, which would be part of a more comprehensive test suite 