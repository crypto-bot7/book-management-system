from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.review import Review, ReviewCreate
from app.models.review import Review as ReviewModel
from app.services.database import get_db

router = APIRouter()

@router.post("/reviews/", response_model=Review)
async def create_review(review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    db_review = ReviewModel(**review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

@router.get("/reviews/{book_id}", response_model=list[Review])
async def read_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ReviewModel).filter(ReviewModel.book_id == book_id))
    reviews = result.scalars().all()
    return reviews