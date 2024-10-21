from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.auth.controllers.auth_check import get_current_user
from app.inventory.schemas.purchase_order_schema import PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse
from app.inventory.controllers.purchase_order_controller import (
    create_purchase_order, update_purchase_order, delete_purchase_order, 
    get_purchase_orders, get_purchase_order
)
from typing import List

router = APIRouter()

@router.get("", response_model=List[PurchaseOrderResponse])
async def list_purchase_orders_route(
    company_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_purchase_orders(db, company_id, skip=skip, limit=limit)

@router.get("/{purchase_order_id}", response_model=PurchaseOrderResponse)
async def read_purchase_order_route(
    purchase_order_id: int,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_purchase_order(db, purchase_order_id, company_id)

@router.post("", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_order_route(
    purchase_order_in: PurchaseOrderCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await create_purchase_order(db, purchase_order_in)

@router.patch("/{purchase_order_id}", response_model=PurchaseOrderResponse)
async def update_purchase_order_route(
    purchase_order_id: int,
    purchase_order_in: PurchaseOrderUpdate,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await update_purchase_order(db, purchase_order_id, company_id, purchase_order_in)

@router.delete("/")
async def delete_purchase_order_route(
    purchase_order_id: int, 
    company_id: int, 
    db: AsyncSession = Depends(get_session), 
    current_user: dict = Depends(get_current_user)
):
    success = await delete_purchase_order(db, purchase_order_id, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return {"message": "Purchase order deleted successfully"}
