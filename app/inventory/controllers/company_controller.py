from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.inventory.models.company import Company
from app.inventory.schemas.company_schema import CompanyCreate, CompanyUpdate

async def get_company(db: AsyncSession, company_id: int):
    return await db.get(Company, company_id)

async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()

async def create_company(db: AsyncSession, company: CompanyCreate):
    db_company = Company(**company.dict())
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return db_company

async def update_company(db: AsyncSession, company_id: int, company: CompanyUpdate):
    db_company = await get_company(db, company_id)
    if db_company:
        for key, value in company.dict(exclude_unset=True).items():
            setattr(db_company, key, value)
        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)
    return db_company

async def delete_company(db: AsyncSession, company_id: int):
    db_company = await get_company(db, company_id)
    if db_company:
        db_company.is_deleted = True
        db.add(db_company)
        await db.commit()
    return db_company
