from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int

class BookCreate(BookBase):
    content: str

class Book(BookBase):
    id: int
    summary: str

    model_config = ConfigDict(from_attributes=True)