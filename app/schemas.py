from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

class BookCreate(BookBase):
    content: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    content: Optional[str] = None

class BookResponse(BookBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: int = Field(ge=1, le=5)

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class SummaryResponse(BaseModel):
    summary: str
    aggregated_rating: Optional[float] = None

class RecommendationRequest(BaseModel):
    genre: Optional[str] = None
    author: Optional[str] = None
    min_rating: Optional[float] = None

class RecommendationResponse(BaseModel):
    books: List[BookResponse]

class GenerateSummaryRequest(BaseModel):
    book_id: int
    content: str

class GenerateSummaryResponse(BaseModel):
    summary: str

class RecommendationFilter(BaseModel):
    genre: Optional[str] = None
    author: Optional[str] = None
    min_rating: Optional[float] = None