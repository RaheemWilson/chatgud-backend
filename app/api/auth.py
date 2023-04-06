from fastapi import APIRouter, HTTPException
from app.schemas.auth import Login, LoginResponse, SignUp

from app.utils.auth import create_access_token, get_password_hash, verify_password
from prisma.models import User
from db import db

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(login: Login):
    try:
        user = await User.prisma().find_first(
            where={
                "email": login.email,
            },
            include={"proficiency": True},
        )
        validated = verify_password(login.password, user.password)
        if validated:
            access_token = create_access_token({"sub": user.id})
            return LoginResponse(user=user, token=access_token)
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/register", response_model=LoginResponse, status_code=201)
async def register(user: SignUp):
    is_user_registered = await User.prisma().find_first(
        where={
            "email": user.email,
        }
    )

    if is_user_registered:
        raise HTTPException(status_code=400, detail="User exists already")

    password = get_password_hash(user.password)

    new_user = await User.prisma().create(
        data={
            "email": user.email,
            "username": user.username,
            "nationality": user.nationality,
            "age": user.age,
            "password": password,
            "proficiency": {"connect": {"id": user.proficiency}},
        },
        include={"proficiency": True},
    )

    if new_user is None:
        raise HTTPException(
            status_code=400, detail="Error occurred during creating user"
        )
    access_token = create_access_token({"sub": new_user.id})

    categories = await db.category.find_many()

    if categories is None:
        return LoginResponse(user=new_user, token=access_token)

    init_categories = [
        {
            "userId": new_user.id,
            "categoryId": category.id,
            "score": 0,
            "completed": 0,
            "proficiencyId": user.proficiency
        }
        for category in categories
    ]
    
    await db.completedcategory.create_many(data=init_categories)

    return LoginResponse(user=new_user, token=access_token)
