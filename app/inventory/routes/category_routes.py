from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.auth.controllers.auth_check import get_current_user
from app.inventory.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.inventory.controllers.category_controller import create_category, update_category, delete_category, get_categories, get_category


router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
async def list_categories_route(
    company_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_categories(db, company_id, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category_route(
    category_id: int,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_category(db, category_id, company_id)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category_route(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await create_category(db, category_in)

@router.patch("/{category_id:int}", response_model=CategoryResponse)
async def update_category_route(
    category_id: int,
    category_in: CategoryUpdate,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await update_category(db, category_id, category_in, company_id)


@router.delete("/")
async def delete_category_route(category_id: int, company_id: int, db: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    success = await delete_category(db, category_id, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}
