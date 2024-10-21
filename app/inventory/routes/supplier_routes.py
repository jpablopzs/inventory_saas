from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.inventory.controllers.supplier_controller import create_supplier, update_supplier, get_suppliers, get_supplier, delete_supplier
from app.inventory.schemas.supplier_schema import SupplierCreate, SupplierUpdate, SupplierResponse
from app.core.database import get_session
from app.auth.controllers.auth_check import get_current_user



router = APIRouter()

@router.get("/", response_model=List[SupplierResponse])
async def list_suppliers_route(
    company_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_suppliers(db, company_id, skip=skip, limit=limit)

@router.get("/{supplier_id}", response_model=SupplierResponse)
async def read_supplier_route(
    supplier_id: int,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_supplier(db, supplier_id, company_id)

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
async def create_supplier_route(
    supplier_in: SupplierCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await create_supplier(db, supplier_in)

@router.patch("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier_route(
    supplier_id: int,
    supplier_in: SupplierUpdate,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await update_supplier(db, supplier_id, supplier_in, company_id)

@router.delete("/")
async def delete_supplier_route(supplier_id: int, company_id: int, db: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    success = await delete_supplier(db, supplier_id, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"message": "Supplier deleted successfully"}
