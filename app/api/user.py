from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, status
from app.schemas.user import UpdateUser, User

from app.utils.auth import get_current_user
from db import db


router = APIRouter()


@router.put("/user", response_model=User, status_code=200)
async def update_user(
    updates: UpdateUser, current_user: User = Depends(get_current_user)
):
    try:
        updated_user = await db.user.update(
            where={"id": current_user.id}, data=updates.dict()
        )
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/user/categories", status_code=200)
async def get_user_categories(current_user: User = Depends(get_current_user)):
    try:
        user_categories = await db.completedcategory.find_many(
            where={"userId": current_user.id}, include={"category": True}
        )
        return user_categories
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
