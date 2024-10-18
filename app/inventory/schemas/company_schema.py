from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    tax_id: str
    phone: str
    email: EmailStr
    txt_address: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    name: Optional[str] = ''
    tax_id: Optional[str] = ''
    phone: Optional[str] = ''
    email: Optional[EmailStr] = ''
    txt_address: Optional[str] = ''

class CompanyResponse(CompanyBase):
    id: int
    create_at: datetime
    update_at: Optional[datetime] = None
    is_deleted: bool

    class Config:
        orm_mode = True