from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException, status
from app.inventory.models.purchase_order import Supplier
from app.inventory.schemas.supplier_schema import SupplierCreate, SupplierUpdate, SupplierResponse
from app.core.database import get_session
from app.auth.controllers.auth_check import get_current_user

async def create_supplier(
    supplier_data: SupplierCreate,
    db: AsyncSession = Depends(get_session)
):
    try:
        supplier = Supplier(**supplier_data.dict())
        db.add(supplier)
        await db.commit()
        await db.refresh(supplier)
        return supplier
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier creation failed"
        )

async def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    company_id: int,
    db: AsyncSession = Depends(get_session)
):
    try:
        result = await db.execute(select(Supplier).filter(Supplier.id == supplier_id, Supplier.company_id == company_id))
        supplier = result.scalars().first()
        
        if supplier is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )
        
        for key, value in supplier_data.dict(exclude_unset=True).items():
            setattr(supplier, key, value)
        
        await db.commit()
        await db.refresh(supplier)
        return supplier
    
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conflict occurred while updating the supplier."
        )

async def get_suppliers(
    company_id: int,
    db: AsyncSession = Depends(get_session)
) -> List[SupplierResponse]:
    result = await db.execute(select(Supplier).filter(Supplier.company_id == company_id))
    suppliers = result.scalars().all()
    return suppliers

async def get_supplier(
    supplier_id: int,
    company_id: int,
    db: AsyncSession = Depends(get_session)
) -> SupplierResponse:
    result = await db.execute(select(Supplier).filter(Supplier.id == supplier_id, Supplier.company_id == company_id))
    supplier = result.scalars().first()

    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    return supplier