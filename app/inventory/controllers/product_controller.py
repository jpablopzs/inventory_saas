from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.inventory.models.inventory import Product
from app.inventory.schemas.product_schema import ProductCreate, ProductUpdate
from app.core.exception_notification import msj_exception

async def get_products(db: AsyncSession, company_id: int, skip: int = 0, limit: int = 10):
    query = select(Product).filter(Product.company_id == company_id).offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    return products

async def get_product(db: AsyncSession, product_id: int, company_id: int):
    query = select(Product).filter(Product.id == product_id, Product.company_id == company_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or does not belong to the specified company."
        )

    return product

async def create_product(db: AsyncSession, product_in: ProductCreate):
    try:
        new_product = Product(**product_in.dict())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product
    
    except Exception as e:
        await msj_exception(db, e)

async def update_product(db: AsyncSession, product_id: int, company_id: int, product_in: ProductUpdate):
    try:
        query = select(Product).filter(Product.id == product_id, Product.company_id == company_id)
        result = await db.execute(query)
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or does not belong to the specified company."
            )

        for key, value in product_in.dict(exclude_unset=True).items():
            setattr(product, key, value)

        await db.commit()
        await db.refresh(product)
        return product
    
    except Exception as e:
        await msj_exception(db, e)

async def delete_product(db: AsyncSession, product_id: int, company_id: int) -> bool:
    try:
        db_product = await get_product(db, product_id, company_id)
        if db_product:
            await db.delete(db_product)
            await db.commit()
            return True
        return False

    except Exception as e:
        await msj_exception(db, e)
