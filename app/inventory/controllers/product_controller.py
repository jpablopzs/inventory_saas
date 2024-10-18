from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.inventory.models.inventory import Product
from app.inventory.schemas.product_schema import ProductCreate, ProductUpdate

async def create_product(db: AsyncSession, product_in: ProductCreate):
    new_product = Product(**product_in.dict())
    db.add(new_product)
    try:
        await db.commit()
        await db.refresh(new_product)
        return new_product
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this code already exists for the company."
        )

async def update_product(db: AsyncSession, product_id: int, company_id: int, product_in: ProductUpdate):
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

    try:
        await db.commit()
        await db.refresh(product)
        return product
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating the product."
        )

async def delete_product(db: AsyncSession, product_id: int, company_id: int):
    query = select(Product).filter(Product.id == product_id, Product.company_id == company_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or does not belong to the specified company."
        )

    product.is_deleted = True
    await db.commit()
    return product

async def list_products(db: AsyncSession, company_id: int, skip: int = 0, limit: int = 10):
    query = select(Product).filter(Product.company_id == company_id).offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    return products

async def read_product(db: AsyncSession, product_id: int, company_id: int):
    query = select(Product).filter(Product.id == product_id, Product.company_id == company_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or does not belong to the specified company."
        )

    return product
