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
    username: str
    gender: Gender
    age: int
    role: Role
    disabled: bool