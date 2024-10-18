from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.inventory.controllers.supplier_controller import create_supplier, update_supplier, get_suppliers, get_supplier
from app.inventory.schemas.supplier_schema import SupplierCreate, SupplierUpdate, SupplierResponse
from app.core.database import get_session
from app.auth.controllers.auth_check import get_current_user



router = APIRouter()

@router.post("", response_model=SupplierResponse)
async def create_new_supplier(
    supplier_data: SupplierCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await create_supplier(supplier_data, db)


@router.patch("/{supplier_id}", response_model=SupplierResponse)
async def update_existing_supplier(
    supplier_id: int,
    company_id: int,
    supplier_data: SupplierUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await update_supplier(supplier_id, supplier_data, company_id, db)

@router.get("/{company_id}", response_model=List[SupplierResponse])
async def list_suppliers(
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_suppliers(company_id, db)

@router.get("/{supplier_id}", response_model=SupplierResponse)
async def retrieve_supplier(
    supplier_id: int,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_supplier(supplier_id, company_id, db)
