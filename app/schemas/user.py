from pydantic import BaseModel
from enum import Enum

class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


class Role(BaseModel):
    id: str
    name: str
    updatedAt: str

class User(BaseModel):
    id: str
    username: str
    email: str
    gender: Gender
    age: int
    nationality: str