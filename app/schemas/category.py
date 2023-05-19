from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    description: str
    image: str
    categoryOrder: int
    intermediateCount: int
    beginnerCount: int