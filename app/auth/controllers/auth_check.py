
import os
import jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Request, status
from typing import Optional, Tuple#, List
from app.auth.models.auth import User
from app.core.database import get_session

#class TokenData(BaseModel):
#    permissions: Optional[List[str]] = None


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
        #token_data = TokenData(permissions=payload.get("permissions", []))
    
    except jwt.PyJWTError as e:
        raise credentials_exception
    
    user = await db.get(User, int(user_id))
    
    if user is None:
        raise credentials_exception
    #return {"user": user, "permissions": token_data.permissions,"admin":user.is_admin}
    return {"user": user}

'''
def has_permission(required_permission: str, current_user: dict):
    user_permissions = current_user.get("permissions", [])
    if required_permission not in user_permissions:
        raise HTTPException(
            status_code=403,
            detail=f"Permission '{required_permission}' is required but not found."
        )
    return True



def check_permissions(current_user,permission_name):
    user = current_user["user"]
    admin = current_user["admin"]
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is not active")
    if not admin:
        has_permission(permission_name, current_user)

'''