from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models, schemas, auth
from ..database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    #Find user by username
    result = await db.execute(select(models.Users).where(models.User.username == form_data.username))
    user = result.scalars().first()
    if not user or auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    #Create access token
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}