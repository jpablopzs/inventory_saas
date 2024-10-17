from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def msj_exception(db: AsyncSession, e: Exception):
    await db.rollback()
    raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")