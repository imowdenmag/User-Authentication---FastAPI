import pytest
import uuid
from fastapi import status

@pytest.mark.asyncio
async def test_register_success(async_client):
    """Test successful user registration"""
    user_data = {
        "username": f"newuser_{uuid.uuid4().hex[:8]}",
        "email": f"newuser_{uuid.uuid4().hex[:8]}@example.com",
        "password": "ValidPass123!"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == user_data["username"]
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_email(async_client, test_user):
    """Test duplicate email registration fails"""
    response = await async_client.post("/register/", json={
        "username": "different_username",
        "email": test_user["email"],  # Using existing email
        "password": "AnotherPass123!"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.json()["detail"].lower()