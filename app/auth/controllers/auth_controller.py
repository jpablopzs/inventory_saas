import bcrypt
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.auth.models.auth import User
from app.auth.controllers.jwt import create_access_token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


async def authenticate_user(db: AsyncSession, email: str, password: str):
    query = await db.execute(select(User).where(User.email == email))
    user = query.scalars().first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user

async def authenticate_and_generate_token(db: AsyncSession, email: str, password: str) -> dict:

    user = await authenticate_user(db, email, password)

    access_token = await create_access_token({"sub": str(user.id)}, db)
    return {"access_token": access_token, "user_id": user.id, "email": user.email}
