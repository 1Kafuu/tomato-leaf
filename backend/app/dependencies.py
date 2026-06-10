from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.crud.user import get_user_by_email
from app.models.user import User
from app.services.supabase_service import get_supabase_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_db():
    if not AsyncSessionLocal:
        raise HTTPException(status_code=500, detail="Database is not configured.")
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not configured")
        
    try:
        response = supabase.auth.get_user(token)
    except Exception:
        raise credentials_exception
        
    if not response or not response.user:
        raise credentials_exception
        
    email = response.user.email
    if not email:
        raise credentials_exception
        
    user = await get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user
