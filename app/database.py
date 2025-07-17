# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL, echo=True)

# Primary session maker (recommended new usage)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Backward compatibility alias
SessionLocal = AsyncSessionLocal  # Add this line

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session