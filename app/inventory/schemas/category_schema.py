from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    company_id: int

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_deleted: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: int
    company_id: int
    create_at: datetime
    update_at: Optional[datetime]
    is_deleted: bool

    class Config:
        orm_mode = True
