from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.inventory.schemas.company_schema import CompanyResponse, CompanyCreate, CompanyUpdate
from app.inventory.controllers.company_controller import get_company, get_companies, create_company, update_company, delete_company
from app.core.database import get_session

router = APIRouter()

@router.get("/companies", response_model=List[CompanyResponse])
async def read_companies(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    return await get_companies(db, skip=skip, limit=limit)

@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def read_company(company_id: int, db: AsyncSession = Depends(get_session)):
    company = await get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/companies", response_model=CompanyResponse)
async def create_company_route(company: CompanyCreate, db: AsyncSession = Depends(get_session)):
    return await create_company(db, company)

@router.patch("/companies/{company_id}", response_model=CompanyResponse)
async def update_company_route(company_id: int, company: CompanyUpdate, db: AsyncSession = Depends(get_session)):
    return await update_company(db, company_id, company)

@router.patch("/companies/delete/", response_model=CompanyResponse)
async def delete_company_route(company_id: int, db: AsyncSession = Depends(get_session)):
    company = await delete_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
