from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SupplierCreate(BaseModel):
    name: str
    email: str
    phone: str
    txt_address: str
    tax_id: str
    company_id: int


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tax_id: Optional[str] = None
    txt_address: Optional[str] = None

class SupplierResponse(SupplierCreate):
    id: int
    create_at: datetime
    update_at: Optional[datetime]

    class Config:
        orm_mode = True
