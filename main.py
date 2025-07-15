from fastapi import FastAPI
from .routers import protected, login, register
from .database import engine, Base

app = FastAPI()

#Include routers
app.include_router(protected.router)
app.include_router(login.router)
app.include_router(register.router)

#Create tables on on startup (for MVP only; use Albermic for production migrations)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)