from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book as BookModel
from app.schemas.book import Book
from app.services.database import get_db

router = APIRouter()

@router.get("/recommendations/", response_model=list[Book])
async def get_recommendations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).limit(5))
    books = result.scalars().all()
    return books