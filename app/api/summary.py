from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from app.models.book import Book as BookModel
from app.models.review import Review as ReviewModel
from app.schemas import SummaryResponse, GenerateSummaryRequest, GenerateSummaryResponse
from app.services.database import get_db
from app.services.llama import generate_summary

router = APIRouter()


@router.get("/books/{book_id}/summary", response_model=SummaryResponse)
async def get_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    # Fetch book
    book = await db.execute(select(BookModel).where(BookModel.id == book_id))
    book = book.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Calculate aggregated rating
    rating = await db.execute(
        select(func.avg(ReviewModel.rating)).where(ReviewModel.book_id == book_id)
    )
    aggregated_rating = rating.scalars().first()

    return SummaryResponse(
        summary=book.summary or "No summary available",
        aggregated_rating=float(aggregated_rating) if aggregated_rating else None
    )


@router.post("/generate-summary", response_model=GenerateSummaryResponse)
async def generate_book_summary(request: GenerateSummaryRequest, db: AsyncSession = Depends(get_db)):
    # Verify book exists
    book = await db.execute(select(BookModel).where(BookModel.id == request.book_id))
    book = book.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Generate summary using Ollama
    summary = await generate_summary(request.content)

    # Update book with new summary
    await db.execute(
        update(BookModel).where(BookModel.id == request.book_id).values(summary=summary)
    )
    await db.commit()

    return GenerateSummaryResponse(summary=summary)