import pytest
from httpx import AsyncClient
from app.main import application as app
from app.services.database import async_session, engine
from app.models.base import Base
from app.models.book import Book
from app.models.review import Review

# todo: mock ollama calls

@pytest.fixture(scope="module")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_book(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/books", json={
            "title": "Test Book",
            "author": "Author",
            "genre": "Fiction",
            "year_published": 2023,
            "content": "Sample content for summary."
        })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"

@pytest.mark.asyncio
async def test_get_books(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_book(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_update_book(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/api/books/1", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

@pytest.mark.asyncio
async def test_delete_book(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/api/books/1")
    assert response.status_code == 204