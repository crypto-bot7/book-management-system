from fastapi import FastAPI
from app.api import books, reviews, recommendations, summary
from app.services.database import engine
from app.models.base import Base


application = FastAPI()

application.include_router(books.router, prefix="/api", tags=["books"])
application.include_router(reviews.router, prefix="/api", tags=["reviews"])
application.include_router(recommendations.router, prefix="/api", tags=["recommendations"])
application.include_router(summary.router, prefix="/api", tags=["summary"])

async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

application.add_event_handler("startup", startup_event)