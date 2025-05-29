import pytest
from httpx import AsyncClient
from app.main import application as app
from app.services.database import async_session, engine
from app.models.base import Base
from app.models.book import Book
from app.models.review import Review
import asyncio
from unittest.mock import patch

@pytest.fixture(scope="module")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_get_summary(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/books/1/summary")
    assert response.status_code == 200
    assert "summary" in response.json()
    assert "aggregated_rating" in response.json()

@pytest.mark.asyncio
async def test_generate_summary(test_db):
    with patch("app.services.llama.generate_summary", return_value="Mocked summary"):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/generate-summary", json={
                "book_id": 1,
                "content": "Sample content"
            })
        assert response.status_code == 200
        assert response.json()["summary"] == "Mocked summary"