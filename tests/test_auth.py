
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app 

@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        #Register a new user
        reg_response = await ac.post("/register/", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        assert reg_response.status_code == 200
        data = reg_response.json()
        assert data["username"] == "testuser"
        assert "id" in data

        #login with new user
        login_response = await ac.post("/login/", data={
            "username": "testuser",
            "password": "testpassword"
        })
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data

        #Access protected route
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        protected_response = await ac.get("/protected/", headers=headers)
        assert protected_response.status_code == 200
        assert "Hello, testuser!" in protected_response.json()["message"]