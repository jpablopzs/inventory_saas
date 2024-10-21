from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PurchaseOrderBase(BaseModel):
    order_code: str
    order_description: Optional[str] = None
    invoice_number: Optional[str] = None
    order_date: Optional[datetime] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    company_id: int
    sumpplier_id: int

class PurchaseOrderUpdate(PurchaseOrderBase):
    order_code: Optional[str] = None
    order_description: Optional[str] = None
    invoice_number: Optional[str] = None
    order_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    is_deleted: Optional[bool] = None

class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    company_id: int
    sumpplier_id: int
    create_at: datetime
    update_at: Optional[datetime]
    is_deleted: Optional[bool] = None

    class Config:
        orm_mode = True
