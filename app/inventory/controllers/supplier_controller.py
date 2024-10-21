from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.inventory.models.purchase_order import Supplier
from app.inventory.schemas.supplier_schema import SupplierCreate, SupplierUpdate
from app.core.exception_notification import msj_exception


async def get_suppliers(db: AsyncSession, company_id: int, skip: int = 0, limit: int = 10):
    query = select(Supplier).filter(Supplier.company_id == company_id).offset(skip).limit(limit)
    result = await db.execute(query)
    supplier = result.scalars().all()
    return supplier

async def get_supplier(db: AsyncSession, supplier_id: int, company_id: int):
    query = select(Supplier).filter(Supplier.id == supplier_id, Supplier.company_id == company_id)
    result = await db.execute(query)
    supplier = result.scalar_one_or_none()

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found or does not belong to the specified company."
        )
    return supplier

async def create_supplier(db: AsyncSession, supplier_in: SupplierCreate):
    try:
        supplier = Supplier(**supplier_in.dict())
        db.add(supplier)
        await db.commit()
        await db.refresh(supplier)
        return supplier

    except Exception as e:
        await msj_exception(db, e)

async def update_supplier( db: AsyncSession, supplier_id: int, supplier_in: SupplierUpdate, company_id: int):
    try:
        result = await db.execute(select(Supplier).filter(Supplier.id == supplier_id, Supplier.company_id == company_id))
        supplier = result.scalars().first()
        
        if supplier is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )
        
        for key, value in supplier_in.dict(exclude_unset=True).items():
            setattr(supplier, key, value)
        
        await db.commit()
        await db.refresh(supplier)
        return supplier
    
    except Exception as e:
        await msj_exception(db, e)

async def delete_supplier(db: AsyncSession, supplier_id: int, company_id: int) -> bool:
    try:
        db_supplier = await get_supplier(db, supplier_id, company_id)
        if db_supplier:
            await db.delete(db_supplier)
            await db.commit()
            return True
        return False

    except Exception as e:
        await msj_exception(db, e)