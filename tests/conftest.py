# tests/conftest.py
import pytest
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import AsyncSessionLocal, Base, engine

@pytest.fixture
async def async_client():
    """Test client fixture (renamed from 'client' to match test usage)"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine("postgresql+asyncpg://postgres:Commando1+@localhost:5432/fastAPI")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(db_engine):
    """Database session fixture (renamed from 'db' to match test usage)"""
    async with AsyncSessionLocal(db_engine) as session:
        async with session.begin():
            yield session

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    """Create all tables before tests and drop them after"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def test_user(async_client):
    """Create and return a test user"""
    user_data = {
        "username": f"testuser_{uuid.uuid4().hex[:8]}",
        "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
        "password": "TestPass123!"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 200
    return user_data

@pytest.fixture
async def auth_headers(async_client, test_user):
    """Auth headers fixture using the renamed async_client"""
    login_res = await async_client.post("/login/", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def cleandup(autouse=True):
    yield
    await db_session.rollback()
