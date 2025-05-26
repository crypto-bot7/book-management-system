from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.book import Book as BookModel
from app.models.review import Review as ReviewModel
from app.schemas import BookResponse, RecommendationFilter
from app.services.database import get_db

router = APIRouter()


@router.get("/recommendations", response_model=list[BookResponse])
async def get_recommendations(filters: RecommendationFilter = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(BookModel)

    # Apply filters
    if filters.genre:
        query = query.where(BookModel.genre == filters.genre)
    if filters.author:
        query = query.where(BookModel.author == filters.author)
    if filters.min_rating:
        subquery = select(ReviewModel.book_id, func.avg(ReviewModel.rating).label("avg_rating")).group_by(
            ReviewModel.book_id).subquery()
        query = query.join(subquery, BookModel.id == subquery.c.book_id).where(
            subquery.c.avg_rating >= filters.min_rating)

    result = await db.execute(query)
    books = result.scalars().all()
    return books