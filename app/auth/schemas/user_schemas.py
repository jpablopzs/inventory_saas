from uuid import UUID
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    username: str
    phone: str
    email: EmailStr
    is_active: bool = False

    class Config:
        from_attributes = True
        
class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    update_at: datetime
    create_at: datetime

    class Config:
        from_attributes = True

class UsersResponse(BaseModel):
    status: str
    data: Dict[str, List[UserRead]]
    message: str

    class Config:
        json_schema_extra  = {
            "example": {
                "status": "200",
                "data": {
                    "users": [
                        {
                            "id": "1",
                            "name": "John Doe",
                            "phone": "+1234567890",
                            "email": "john.smith@example.com",
                            "is_active": True,
                            "update_at": "2024-09-17T16:09:41.638Z",
                            "create_at": "2024-09-17T16:09:41.638Z"
                        }
                    ]
                },
                "message": "Users List"
            }
        }
        

class UserUpdate(UserBase):
    name: Optional[str] = None 
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
