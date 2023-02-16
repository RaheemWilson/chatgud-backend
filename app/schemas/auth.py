from typing import Dict
from pydantic import BaseModel
from app.schemas.user import User

class Login(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    user: User
    token: str