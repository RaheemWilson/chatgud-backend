from typing import Dict, Optional
from pydantic import BaseModel
from app.schemas.user import Gender, User

class Login(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    user: User
    token: str
    
class SignUp(BaseModel):
    email: str
    username: str
    password: str
    age: int
    nationality: str
    proficiency: Optional[str]
    