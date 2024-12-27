from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text  # Import `text`

from app.core.security.verify_secret import verify_secret
from app.database.connection import get_db

router = APIRouter()


@router.get("/test-db")
async def test_db(session: AsyncSession = Depends(get_db), x_secret_key: str = Depends(verify_secret)):
    # Use `text` for the raw SQL query
    result = await session.execute(text("SELECT NOW()"))
    current_time = result.scalar()
    return {"current_time": current_time}