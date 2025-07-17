from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, auth
from app.database import AsyncSessionLocal as SessionLocal

router = APIRouter(
    prefix="/protected",
    tags=["protected"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

async def get_db():
    async with SessionLocal() as session: 
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await db.execute(select(models.User).where(models.User.username == username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/", summary="Protected route example")
async def read_protected_route(current_user: models.User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}! This is a protected route."}