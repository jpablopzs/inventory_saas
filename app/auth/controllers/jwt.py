import os
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.future import select
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone

async def create_access_token(data: dict, db: AsyncSession) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=int(os.environ.get('JWT_EXPIRATION')))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get('JWT_SECRET'), algorithm=os.environ.get('JWT_ALGORITHM'))
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms=[os.environ.get('JWT_ALGORITHM')])
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

