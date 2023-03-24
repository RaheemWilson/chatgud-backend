from fastapi import APIRouter, HTTPException
from app.schemas.auth import Login, LoginResponse, SignUp

from app.utils.auth import create_access_token, get_password_hash, verify_password
from prisma.models import User

router = APIRouter()

@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(login: Login):
    try:
        user = await User.prisma().find_first(
            where={
                "email": login.email,
            }
        )
        validated = verify_password(login.password, user.password)
        if validated:
            access_token = create_access_token({ 'sub': user.id })
            return LoginResponse(user=user, token=access_token)
    except:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    
@router.post("/register", response_model=LoginResponse, status_code=201)
async def register(user: SignUp):
    is_user_registered = await User.prisma().find_first(
        where={
            "email": user.email,
        }
    )
    
    if is_user_registered: 
        raise HTTPException(status_code=400, detail='User exists already')
    
    password = get_password_hash(user.password)
        
    new_user = await User.prisma().create(
        data={
            'email': user.email,
            'username': user.username,
            'nationality': user.nationality,
            'age': user.age,
            'password': password,
            'proficiency': {
                'connect': {
                    'id': user.proficiency
                }
            }
        }
    )
    
    if new_user is None:
        raise HTTPException(status_code=400, detail='Error occurred during creating user')
    
    access_token = create_access_token({ 'sub': new_user.id })
    del new_user.password
    
    return LoginResponse(user=new_user, token=access_token)
    
    
    

