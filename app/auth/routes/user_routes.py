from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.auth.schemas.user_schemas import UserCreate, UserRead, UserUpdate, UsersResponse
from app.auth.controllers.user_controller import create_user, get_user, get_users, update_user, delete_user
from app.auth.controllers.auth_check import get_current_user#, check_permissions


router = APIRouter()

@router.post("", response_model=UserRead)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await create_user(db, user)

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    #check_permissions(current_user, "user:readId")
    db_user = await get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("", response_model=UsersResponse)
async def read_users(db: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    #check_permissions(current_user, "user:list")
    users = await get_users(db)
    users_pydantic = [UserRead.model_validate(user) for user in users]
    return {
        "status": "200",
        "data": {
            "users": users_pydantic,
        },
        "message": "Users List",
    }

@router.patch("/{user_id}", response_model=UserRead)
async def update_user_endpoint(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    #check_permissions(current_user, "user:update")
    db_user = await update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    #check_permissions(current_user, "user:delete")
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
