from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book as BookModel
from app.schemas.book import Book
from app.services.database import get_db

router = APIRouter()

@router.get("/books/{book_id}/summary", response_model=Book)
async def get_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).filter(BookModel.id == book_id))
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book