# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool  # Add this import

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Configure engine with these key parameters
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool,  # Disable connection pooling for tests
    connect_args={
        "prepared_statement_cache_size": 0,  # Disable server-side statement caching
        "statement_cache_size": 0,  # Disable client-side statement caching
    }
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    """Async database session dependency with proper cleanup"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Commit if no exceptions
        except Exception:
            await session.rollback()  # Rollback on errors
            raise
        finally:
            await session.close()  # Ensure session is closed