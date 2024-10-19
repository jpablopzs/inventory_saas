from sqlite3 import IntegrityError
import bcrypt
from typing import List
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from app.auth.models.auth import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.schemas.user_schemas import UserCreate, UserRead, UserUpdate
from app.core.exception_notification import msj_exception


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

async def create_user(db: AsyncSession, user: UserCreate) -> UserRead:
    user.password = hash_password(user.password)
    db_user = User(**user.model_dump())
    db.add(db_user)

    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await db.rollback()
        await msj_exception(db, e)

async def get_user(db: AsyncSession, user_id: int) -> UserRead:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession) -> List[UserRead]:
    result = await db.execute(select(User))
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    try:
        db_user = await db.get(User, user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db_user.update_at = datetime.now()
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user
    
    except IntegrityError as e:
        await db.rollback()
        await msj_exception(db, e)
    
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
