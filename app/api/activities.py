from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, status
from pydantic import BaseModel
from app.schemas.user import User
from app.utils.auth import get_current_user
from db import db

router = APIRouter()


class SuccessResponse(BaseModel):
    success: bool


class UpdateCategory(BaseModel):
    completed: int
    categoryId: str
    proficiencyId: str


@router.put("/category", status_code=200, response_model=SuccessResponse)
async def update_user_category(
    data: UpdateCategory, current_user: User = Depends(get_current_user)
):
    try:
        score = data.completed * 10
        await db.completedcategory.update_many(
            where={
                "AND": [
                    {"categoryId": data.categoryId},
                    {"proficiencyId": data.proficiencyId},
                    {"userId": current_user.id},
                ]
            },
            data={"completed": data.completed, "score": score},
        )

        return SuccessResponse(success=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
