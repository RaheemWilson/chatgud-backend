from typing import List
from fastapi import APIRouter, Depends

from app.schemas.task import Task
from app.schemas.user import User
from app.utils.auth import get_current_user
from db import db

router = APIRouter()


@router.get("/tasks/{categoryId}", response_model=List[Task], status_code=200)
async def get_category(categoryId: str, current_user: User = Depends(get_current_user)):
    return await db.task.find_many(
        where={
            "AND": [
                {"categoryId": categoryId},
                {"proficiencyId": current_user.proficiencyId},
            ]
        },
        include={
            "answer": True,
            "taskChoice": {"include": {"choices": True}},
        },
    )
