from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime

class PurchaseOrderDetailBase(BaseModel):
    product_quantity: int
    unit_price: condecimal(max_digits=10, decimal_places=2)
    total_price: condecimal(max_digits=10, decimal_places=2)
    is_deleted: Optional[bool] = False

class PurchaseOrderDetailCreate(PurchaseOrderDetailBase):
    company_id: int
    product_id: int
    purchase_order_id: int

class PurchaseOrderDetailUpdate(PurchaseOrderDetailBase):
    product_quantity: Optional[int] = None
    unit_price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    total_price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    is_deleted: Optional[bool] = None

class PurchaseOrderDetailResponse(PurchaseOrderDetailBase):
    id: int
    company_id: int
    product_id: int
    purchase_order_id: int
    create_at: datetime
    update_at: Optional[datetime]
    is_deleted: Optional[bool] = None

    class Config:
        orm_mode = True
