import pytest
import uuid
from fastapi import status

@pytest.mark.asyncio
async def test_full_flow(async_client):
    """Test complete registration → login → protected route flow"""
    # Generate unique test data
    unique_id = uuid.uuid4().hex[:8]
    user_data = {
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "SecurePass123!"  # 12+ chars with upper/lower/special
    }
    
    # Test registration
    reg_res = await async_client.post("/register/", json=user_data)
    print("Registration Response:", reg_res.json())
    assert reg_res.status_code == status.HTTP_200_OK
    assert reg_res.json()["email"] == user_data["email"]
    assert "id" in reg_res.json()
    
    # Test duplicate registration
    dup_res = await async_client.post("/register/", json=user_data)
    assert dup_res.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in dup_res.json()["detail"].lower()
    
    # Test login
    login_res = await async_client.post("/login/", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    assert login_res.status_code == status.HTTP_200_OK
    assert "access_token" in login_res.json()
    
    # Test protected route
    token = login_res.json()["access_token"]
    protected_res = await async_client.get("/protected/", headers={
        "Authorization": f"Bearer {token}"
    })
    assert protected_res.status_code == status.HTTP_200_OK