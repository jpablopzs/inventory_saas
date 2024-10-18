from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    product_code: str
    name: str
    description: Optional[str] = None
    current_price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    stock_quantity: Optional[int] = None

class ProductCreate(ProductBase):
    company_id: int
    category_id: int

class ProductUpdate(ProductBase):
    product_code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    current_price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    stock_quantity: Optional[int] = None
    is_deleted: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    company_id: int
    category_id: int
    create_at: datetime
    update_at: Optional[datetime]
    is_deleted: bool

    class Config:
        orm_mode = True
