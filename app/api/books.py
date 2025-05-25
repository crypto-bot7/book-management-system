from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.book import Book, BookCreate
from app.models.book import Book as BookModel
from app.services.database import get_db
from app.services.llama import generate_summary

router = APIRouter()

@router.post("/books/", response_model=Book)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    summary = await generate_summary(book.content)
    db_book = BookModel(
        title=book.title,
        author=book.author,
        genre=book.genre,
        year_published=book.year_published,
        summary=summary
    )
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.id == book_id))
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/books/", response_model=list[Book])
async def read_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel))
    books = result.scalars().all()
    return books

@router.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: BookCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.id == book_id))
    db_book = result.scalar_one_or_none()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = book.title
    db_book.author = book.author
    db_book.genre = book.genre
    db_book.year_published = book.year_published
    db_book.summary = await generate_summary(book.content)
    
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.id == book_id))
    db_book = result.scalar_one_or_none()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await db.delete(db_book)
    await db.commit()
    return {"detail": "Book deleted successfully"}

