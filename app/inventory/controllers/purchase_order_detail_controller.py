from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.inventory.models.purchase_order import PurchaseOrderDetail
from app.inventory.schemas.purchase_order_detail_schema import PurchaseOrderDetailCreate, PurchaseOrderDetailUpdate
from app.core.exception_notification import msj_exception

async def get_purchase_order_details(db: AsyncSession, purchase_order_id: int, company_id: int, skip: int = 0, limit: int = 10):
    query = select(PurchaseOrderDetail).filter(PurchaseOrderDetail.purchase_order_id == purchase_order_id, PurchaseOrderDetail.company_id == company_id).offset(skip).limit(limit)
    result = await db.execute(query)
    purchase_order_details = result.scalars().all()
    return purchase_order_details

async def get_purchase_order_detail(db: AsyncSession, purchase_order_detail_id: int, company_id: int):
    query = select(PurchaseOrderDetail).filter(PurchaseOrderDetail.id == purchase_order_detail_id, PurchaseOrderDetail.company_id == company_id)
    result = await db.execute(query)
    purchase_order_detail = result.scalar_one_or_none()

    if not purchase_order_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase Order Detail not found or does not belong to the specified company."
        )

    return purchase_order_detail

async def create_purchase_order_detail(db: AsyncSession, purchase_order_detail_in: PurchaseOrderDetailCreate):
    try:
        new_purchase_order_detail = PurchaseOrderDetail(**purchase_order_detail_in.dict())
        db.add(new_purchase_order_detail)
        await db.commit()
        await db.refresh(new_purchase_order_detail)
        return new_purchase_order_detail
    
    except Exception as e:
        await msj_exception(db, e)

async def update_purchase_order_detail(db: AsyncSession, purchase_order_detail_id: int, purchase_order_id: int, company_id: int, purchase_order_detail_in: PurchaseOrderDetailUpdate):
    try:
        query = select(PurchaseOrderDetail).filter(PurchaseOrderDetail.id == purchase_order_detail_id, PurchaseOrderDetail.purchase_order_id == purchase_order_id, PurchaseOrderDetail.company_id == company_id)
        result = await db.execute(query)
        purchase_order_detail = result.scalar_one_or_none()

        if not purchase_order_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase Order Detail not found or does not belong to the specified company."
            )

        for key, value in purchase_order_detail_in.dict(exclude_unset=True).items():
            setattr(purchase_order_detail, key, value)

        await db.commit()
        await db.refresh(purchase_order_detail)
        return purchase_order_detail
    
    except Exception as e:
        await msj_exception(db, e)

async def delete_purchase_order_detail(db: AsyncSession, purchase_order_detail_id: int, company_id: int) -> bool:
    try:
        db_purchase_order_detail = await get_purchase_order_detail(db, purchase_order_detail_id, company_id)
        if db_purchase_order_detail:
            await db.delete(db_purchase_order_detail)
            await db.commit()
            return True
        return False

    except Exception as e:
        await msj_exception(db, e)
