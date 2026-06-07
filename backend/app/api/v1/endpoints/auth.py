from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, Token
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import get_user_by_email, create_user
from app.dependencies import get_db
from app.services.supabase_service import get_supabase_client

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not configured")
        
    db_user = await get_user_by_email(db, email=request.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered in local DB")
    
    # Register with Supabase
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    if not response.user:
        raise HTTPException(status_code=400, detail="Failed to register user in Supabase")
        
    user_id = response.user.id
    
    # Save to local DB with the Supabase UUID
    user_create = UserCreate(email=request.email, password=request.password, full_name=request.full_name)
    user = await create_user(db=db, user=user_create, user_id=user_id)
    return user

@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not configured")
        
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not response.session:
        raise HTTPException(status_code=401, detail="Authentication failed")
        
    user = await get_user_by_email(db, email=request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found in local DB")
        
    access_token = response.session.access_token
    return Token(access_token=access_token, token_type="bearer", user=user)
