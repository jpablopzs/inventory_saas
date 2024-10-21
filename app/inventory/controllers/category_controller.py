from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.inventory.models.inventory import Category
from app.inventory.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.core.exception_notification import msj_exception

async def get_categories(db: AsyncSession, company_id: int, skip: int = 0, limit: int = 10):
    query = select(Category).filter(Category.company_id == company_id).offset(skip).limit(limit)
    result = await db.execute(query)
    categories = result.scalars().all()
    return categories

async def get_category(db: AsyncSession, category_id: int, company_id: int):
    query = select(Category).filter(Category.id == category_id, Category.company_id == company_id)
    result = await db.execute(query)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or does not belong to the specified company."
        )

    return category

async def create_category(db: AsyncSession, category_in: CategoryCreate):
    try:
        new_category = Category(**category_in.dict())
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        return new_category

    except Exception as e:
        await msj_exception(db, e)

async def update_category(
    db: AsyncSession, category_id: int, category_in: CategoryUpdate, company_id: int):
    try:
        query = select(Category).filter(Category.id == category_id, Category.company_id == company_id)
        result = await db.execute(query)
        category = result.scalar_one_or_none()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or does not belong to the specified company."
            )

        for key, value in category_in.dict(exclude_unset=True).items():
            setattr(category, key, value)

        db.add(category)
        await db.commit()
        await db.refresh(category)

        return category
    except Exception as e:
        await msj_exception(db, e)

async def delete_category(db: AsyncSession, category_id: int, company_id: int) -> bool:
    try:
        db_category = await get_category(db, category_id, company_id)
        if db_category:
            await db.delete(db_category)
            await db.commit()
            return True
        return False

    except Exception as e:
        await msj_exception(db, e)
