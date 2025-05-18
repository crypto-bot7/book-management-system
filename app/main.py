from fastapi import FastAPI
from app.api import books, reviews, recommendations, summary
from app.services.database import engine, Base

app = FastAPI()

app.include_router(books.router, prefix="/api", tags=["books"])
app.include_router(reviews.router, prefix="/api", tags=["reviews"])
app.include_router(recommendations.router, prefix="/api", tags=["recommendations"])
app.include_router(summary.router, prefix="/api", tags=["summary"])

async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.add_event_handler("startup", startup_event)