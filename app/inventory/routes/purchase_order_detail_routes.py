from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.auth.controllers.auth_check import get_current_user
from app.inventory.schemas.purchase_order_detail_schema import PurchaseOrderDetailCreate, PurchaseOrderDetailUpdate, PurchaseOrderDetailResponse
from app.inventory.controllers.purchase_order_detail_controller import create_purchase_order_detail, update_purchase_order_detail, delete_purchase_order_detail, get_purchase_order_details, get_purchase_order_detail
from typing import List

router = APIRouter()

@router.get("", response_model=List[PurchaseOrderDetailResponse])
async def list_purchase_order_details_route(
    purchase_order_id: int,
    company_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_purchase_order_details(db, purchase_order_id, company_id, skip=skip, limit=limit)

@router.get("/{purchase_order_detail_id}", response_model=PurchaseOrderDetailResponse)
async def read_purchase_order_detail_route(
    purchase_order_detail_id: int,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_purchase_order_detail(db, purchase_order_detail_id, company_id)

@router.post("", response_model=PurchaseOrderDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_order_detail_route(
    purchase_order_detail_in: PurchaseOrderDetailCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await create_purchase_order_detail(db, purchase_order_detail_in)

@router.patch("/", response_model=PurchaseOrderDetailResponse)
async def update_purchase_order_detail_route(
    purchase_order_detail_id: int,
    purchase_order_id: int,
    purchase_order_detail_in: PurchaseOrderDetailUpdate,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await update_purchase_order_detail(db, purchase_order_detail_id, purchase_order_id, company_id, purchase_order_detail_in)

@router.delete("/")
async def delete_purchase_order_detail_route(
    purchase_order_detail_id: int,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    success = await delete_purchase_order_detail(db, purchase_order_detail_id, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Purchase Order Detail not found")
    return {"message": "Purchase Order Detail deleted successfully"}
