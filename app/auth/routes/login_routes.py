from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.auth.schemas.login_schemas import UserLogin
from app.auth.controllers.auth_controller import authenticate_and_generate_token

router = APIRouter()

@router.post("/")
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_session)):
   result = await authenticate_and_generate_token(db, user_login.email, user_login.password)
   return {
      "status": "200",
      "data": {
      "email": result["email"],
      "user_id": result["user_id"],
      "access_token": result["access_token"]
      },
      "message": "Login successful",
      }
