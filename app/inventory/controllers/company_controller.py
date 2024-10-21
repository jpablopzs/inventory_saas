from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.inventory.models.company import Company
from app.inventory.schemas.company_schema import CompanyCreate, CompanyUpdate, CompanyResponse
from app.core.exception_notification import msj_exception

async def get_company(db: AsyncSession, company_id: int) -> CompanyResponse:
    result = await db.execute(select(Company).filter(Company.id == company_id))
    return result.scalar_one_or_none()

async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()

async def create_company(db: AsyncSession, company: CompanyCreate):
    try:
        db_company = Company(**company.dict())
        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)
        return db_company
    except Exception as e:
        await msj_exception(db, e)

async def update_company(db: AsyncSession, company_id: int, company: CompanyUpdate):
    try:
        db_company = await get_company(db, company_id)
        if db_company:
            for key, value in company.dict(exclude_unset=True).items():
                setattr(db_company, key, value)
            db.add(db_company)
            await db.commit()
            await db.refresh(db_company)
        return db_company

    except Exception as e:
        await msj_exception(db, e)

async def delete_company(db: AsyncSession, company_id: int) -> bool:
    try:
        db_company = await get_company(db, company_id)
        if db_company:
            await db.delete(db_company)
            await db.commit()
            return True
        return False

    except Exception as e:
        await msj_exception(db, e)
