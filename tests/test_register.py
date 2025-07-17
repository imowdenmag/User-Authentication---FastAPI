import pytest
import uuid
from fastapi import status

@pytest.mark.asyncio
async def test_register_success(async_client, db_session):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "ValidPass123!"
    }
    async with db_session.begin():
        response = await async_client.post("/register/", json=user_data)
        assert response.status_code == 200

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