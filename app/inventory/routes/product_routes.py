from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.auth.controllers.auth_check import get_current_user
from app.inventory.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.inventory.controllers.product_controller import create_product, update_product, delete_product, get_products, get_product
from typing import List

router = APIRouter()

@router.get("", response_model=List[ProductResponse])
async def list_products_route(
    company_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_products(db, company_id, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product_route(
    product_id: int,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await get_product(db, product_id, company_id)

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product_route(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await create_product(db, product_in)

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product_route(
    product_id: int,
    product_in: ProductUpdate,
    company_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await update_product(db, product_id, company_id, product_in)

@router.delete("/")
async def delete_product_route(product_id: int, company_id: int, db: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    success = await delete_product(db, product_id, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
