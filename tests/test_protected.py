import pytest

@pytest.mark.asyncio
async def test_protected_route_success(async_client, auth_headers):
    response = await async_client.get("/protected/", headers=auth_headers)
    assert response.status_code == 200
    assert "Hello," in response.json()["message"]

@pytest.mark.asyncio
async def test_protected_route_no_token(async_client):
    response = await async_client.get("/protected/")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_route_invalid_token(async_client):
    response = await async_client.get(
        "/protected/",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401