from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schemas, auth
from ..database import get_db  # Use the centralized get_db function

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@router.post("/", response_model=schemas.Token)  # Use Token schema
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # Find user by username (fixed model.Users to models.User)
    result = await db.execute(
        select(models.User).where(models.User.username == form_data.username)
    )
    user = result.scalars().first()

    # Fixed password verification logic
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},  # Required for OAuth2
        )
    
    # Create access token
    access_token = auth.create_access_token(
        data={"sub": user.username}  # Standard JWT subject claim
    )
    return {"access_token": access_token, "token_type": "bearer"}