import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import initiate_database, close_database
from app.inventory.routes import company_routes
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

app.include_router(company_routes.router, prefix="/api", tags=["Companies"])
