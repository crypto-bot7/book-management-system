from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.models.review import Review as ReviewModel
from app.models.book import Book as BookModel
from app.schemas import ReviewCreate, ReviewResponse
from app.services.database import get_db

router = APIRouter()


@router.post("/books/{book_id}/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(book_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    # Check if book exists
    book = await db.execute(select(BookModel).where(BookModel.id == book_id))
    if not book.scalars().first():
        raise HTTPException(status_code=404, detail="Book not found")

    # Create review
    stmt = insert(ReviewModel).values(book_id=book_id, **review.dict()).returning(ReviewModel)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()


@router.get("/books/{book_id}/reviews", response_model=list[ReviewResponse])
async def get_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    # Check if book exists
    book = await db.execute(select(BookModel).where(BookModel.id == book_id))
    if not book.scalars().first():
        raise HTTPException(status_code=404, detail="Book not found")

    result = await db.execute(select(ReviewModel).where(ReviewModel.book_id == book_id))
    return result.scalars().all()