import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import initiate_database, close_database
from app.auth.routes import user_routes, login_routes
from app.inventory.routes import (company_routes, 
                                  category_routes,
                                  product_routes,
                                  supplier_routes,
                                  purchase_order_routes,
                                  purchase_order_detail_routes) 

env = os.getenv("ENV", "development")

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await initiate_database()
    yield
    await close_database()

if env == "production":
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI(lifespan=app_lifespan)

origins = [
    os.environ.get('CSRF_FRONT')
]

app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])
app.include_router(login_routes.router, prefix="/api/login", tags=["Login"])
app.include_router(company_routes.router, prefix="/api/companies", tags=["Companies"])
app.include_router(category_routes.router, prefix="/api/category", tags=["Categories"])
app.include_router(product_routes.router, prefix="/api/product", tags=["Products"])
app.include_router(supplier_routes.router, prefix="/api/supplier", tags=["Suppliers"])
app.include_router(purchase_order_routes.router, prefix="/api/purchase_order", tags=["Purchase Orders"])
app.include_router(purchase_order_detail_routes.router, prefix="/api/purchase_order_detail", tags=["Purchase Orders Detail"])
