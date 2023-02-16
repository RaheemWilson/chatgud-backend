from fastapi import APIRouter, HTTPException
from app import prisma
from app.schemas.auth import Login, LoginResponse

from app.schemas.user import User
from app.utils.auth import create_access_token, verify_password

router = APIRouter()

@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(login: Login):
    try:
        user = await prisma.user.find_first(
            where={
                "email": login.email,
            }
        )
        validated = verify_password(login.password, user.password)
        del user.password
        if validated:
                access_token = create_access_token({ 'sub': user.id })
                return LoginResponse(user=User, token=access_token)
    except:
        raise HTTPException(status_code=401, detail='Invalid credentials')

