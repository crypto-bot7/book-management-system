from pydantic import BaseModel, ConfigDict

class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)