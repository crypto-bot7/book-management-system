from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from app.models.book import Book as BookModel
from app.schemas import BookCreate, BookUpdate, BookResponse
from app.services.database import get_db
from app.services.llama import generate_summary

router = APIRouter()

@router.post("/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    book_data = book.dict(exclude={"content"})
    if book.content:
        summary = await generate_summary(book.content)
        book_data["summary"] = summary
    stmt = insert(BookModel).values(**book_data).returning(BookModel)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()

@router.get("/books", response_model=list[BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel))
    return result.scalars().all()

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=BookUpdate)
async def update_book(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    update_data = book.dict(exclude_unset=True, exclude={"content"})
    if book.content:
        summary = await generate_summary(book.content)
        update_data["summary"] = summary
    stmt = update(BookModel).where(BookModel.id == book_id).values(**update_data).returning(BookModel)
    result = await db.execute(stmt)
    await db.commit()
    updated_book = result.scalars().first()
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(BookModel).where(BookModel.id == book_id)
    result = await db.execute(stmt)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return None