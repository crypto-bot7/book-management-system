import pytest
from httpx import AsyncClient
from app.main import application as app
from app.services.database import async_session, engine
from app.models.base import Base
from app.models.book import Book
from app.models.review import Review
import asyncio

@pytest.fixture(scope="module")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_review(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/books/1/reviews", json={
            "user_id": 1,
            "review_text": "Great book!",
            "rating": 5
        })
    assert response.status_code == 201
    assert response.json()["review_text"] == "Great book!"

@pytest.mark.asyncio
async def test_get_reviews(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/books/1/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)