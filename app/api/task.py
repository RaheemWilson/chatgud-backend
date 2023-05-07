from typing import List
from fastapi import APIRouter, Depends

from app.schemas.task import DailyChallenge, Quiz, Task
from app.schemas.user import User
from app.utils.auth import get_current_user
from db import db

router = APIRouter()


@router.get("/tasks/courses/{categoryId}", response_model=List[Task], status_code=200)
async def get_category(categoryId: str, current_user: User = Depends(get_current_user)):
    return await db.task.find_many(
        where={
            "AND": [
                {"categoryId": categoryId},
                {"proficiencyId": current_user.proficiencyId},
                {"taskType": "course"}
            ]
        },
        include={
            "answer": True,
            "taskChoice": {"include": {"choices": True}},
        },
    )


@router.get("/tasks/quizzes/{quizId}", response_model=Quiz, status_code=200)
async def get_quiz(quizId: str, current_user: User = Depends(get_current_user)):
    return await db.quiz.find_unique(
        where={
            "id": quizId,
        },
        include={
            "quizQuestion": {
                "include": {
                    "task": {
                        "include": {
                            "taskChoice": {"include": {"choices": True}},
                            "answer": True,
                        }
                    },
                    "questionResource": True,
                }
            },
        },
    )


@router.get("/tasks/quizzes", response_model=List[Quiz], status_code=200)
async def get_quiz(current_user: User = Depends(get_current_user)):
    return await db.quiz.find_many(
        where={
            "proficiencyId": current_user.proficiencyId,
        },
        include={
            "quizQuestion": {
                "include": {
                    "task": {
                        "include": {
                            "taskChoice": {"include": {"choices": True}},
                            "answer": True,
                        }
                    }
                }
            },
        },
    )


@router.get("/tasks/challenges", response_model=List[DailyChallenge], status_code=200)
async def get_quiz(dayOrder: int, current_user: User = Depends(get_current_user)):
    return await db.dailychallenge.find_many(
        where={
            "AND": [
                {"problem": {"proficiencyId": current_user.proficiencyId}},
                {"dayOrder": dayOrder},
            ]
        },
        include={
            "problem": {
                "include": {
                    "taskChoice": {"include": {"choices": True}},
                    "answer": True,
                }
            },
        },
    )
