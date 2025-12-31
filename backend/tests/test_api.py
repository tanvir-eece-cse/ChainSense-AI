"""
Backend tests for ChainSense-AI.
"""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_root_endpoint():
    """Test the root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "ChainSense-AI" in data["message"]


@pytest.mark.anyio
async def test_health_endpoint():
    """Test the health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.anyio
async def test_liveness_endpoint():
    """Test the liveness probe endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/health/live")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


@pytest.mark.anyio
async def test_register_user_validation():
    """Test user registration validation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test with invalid email
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "username": "testuser",
                "password": "ValidPass123",
            }
        )
    
    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent@test.com",
                "password": "wrongpassword",
            }
        )
    
    assert response.status_code == 401
