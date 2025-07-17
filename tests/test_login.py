# tests/test_login.py
import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_login_success(async_client, test_user):
    """Test successful login with correct credentials"""
    # Note the removed trailing slash in "/login" to match your router
    response = await async_client.post(
        "/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    
    # Verify token is valid
    token = data["access_token"]
    assert len(token.split(".")) == 3  # Valid JWT has 3 parts

@pytest.mark.asyncio
async def test_login_wrong_password(async_client, test_user):
    """Test login fails with incorrect password"""
    response = await async_client.post(
        "/login",
        data={
            "username": test_user["username"],
            "password": "wrong_password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == "Bearer"

@pytest.mark.asyncio
async def test_login_nonexistent_user(async_client):
    """Test login fails with non-existent username"""
    response = await async_client.post(
        "/login",
        data={
            "username": "nonexistent_user",
            "password": "any_password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]