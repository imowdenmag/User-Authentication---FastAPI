from fastapi import FastAPI
from app.routers import protected, login, register
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#CORS middleware setup
origins = [
    "http://localhost:3000", # Your frontend dev server (React, Vue, etc.)
    "http://localhost:5173", #Vite
    #Add morr origins as needed, or use "*" for all origins (not recommended for production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Include routers
app.include_router(protected.router)
app.include_router(login.router)
app.include_router(register.router)

#Create tables on on startup (for MVP only; use Albermic for production migrations)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)