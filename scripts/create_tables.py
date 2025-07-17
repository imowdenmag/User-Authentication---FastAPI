import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine, Base
from app import models

async def create():
    print("Database URL:", engine.url)
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(create())
    