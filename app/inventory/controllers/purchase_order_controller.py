from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.inventory.models.purchase_order import PurchaseOrder
from app.inventory.schemas.purchase_order_schema import PurchaseOrderCreate, PurchaseOrderUpdate
from app.core.exception_notification import msj_exception

async def get_purchase_orders(db: AsyncSession, company_id: int, skip: int = 0, limit: int = 10):
    query = select(PurchaseOrder).filter(PurchaseOrder.company_id == company_id).offset(skip).limit(limit)
    result = await db.execute(query)
    purchase_orders = result.scalars().all()
    return purchase_orders

async def get_purchase_order(db: AsyncSession, purchase_order_id: int, company_id: int):
    query = select(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id, PurchaseOrder.company_id == company_id)
    result = await db.execute(query)
    purchase_order = result.scalar_one_or_none()

    if not purchase_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found or does not belong to the specified company."
        )

    return purchase_order

async def create_purchase_order(db: AsyncSession, purchase_order_in: PurchaseOrderCreate):
    try:
        new_purchase_order = PurchaseOrder(**purchase_order_in.dict())
        db.add(new_purchase_order)
        await db.commit()
        await db.refresh(new_purchase_order)
        return new_purchase_order
    
    except Exception as e:
        await msj_exception(db, e)

async def update_purchase_order(db: AsyncSession, purchase_order_id: int, company_id: int, purchase_order_in: PurchaseOrderUpdate):
    try:
        query = select(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id, PurchaseOrder.company_id == company_id)
        result = await db.execute(query)
        purchase_order = result.scalar_one_or_none()

        if not purchase_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase order not found or does not belong to the specified company."
            )

        for key, value in purchase_order_in.dict(exclude_unset=True).items():
            setattr(purchase_order, key, value)

        await db.commit()
        await db.refresh(purchase_order)
        return purchase_order
    
    except Exception as e:
        await msj_exception(db, e)

async def delete_purchase_order(db: AsyncSession, purchase_order_id: int, company_id: int) -> bool:
    try:
        db_purchase_order = await get_purchase_order(db, purchase_order_id, company_id)
        if db_purchase_order:
            await db.delete(db_purchase_order)
            await db.commit()
            return True
        return False

    except Exception as e:
        await msj_exception(db, e)
