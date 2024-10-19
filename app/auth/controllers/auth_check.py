
import os
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Request, status
from typing import Optional, Tuple
from app.auth.models.auth import User
from app.core.database import get_session

def get_authorization_scheme_param(authorization_header_value: Optional[str]) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


async def header_bearer(request: Request) -> Optional[str]:
    authorization = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


async def get_current_user(token: str = Depends(header_bearer), db: AsyncSession = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms=os.environ.get('JWT_ALGORITHM'))
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    
    except jwt.PyJWTError as e:
        raise credentials_exception
    
    user = await db.get(User, int(user_id))
    
    if user is None:
        raise credentials_exception
    return {"user": user}
