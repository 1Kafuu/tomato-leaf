from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
import uuid

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate, user_id: str | None = None) -> User:
    db_user = User(
        email=user.email,
        full_name=user.full_name
    )
    if user_id:
        db_user.id = uuid.UUID(user_id)
        
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
