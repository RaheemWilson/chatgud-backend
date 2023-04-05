from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

from app.schemas.proficiency import Proficiency

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
    age: int
    nationality: str
    dateCreated: datetime
    proficiency: Optional[Proficiency]
    
class UpdateUser(BaseModel):
    username: str
    age: int
    nationality: str
    
