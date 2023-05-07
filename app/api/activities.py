from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, status
from pydantic import BaseModel
from app.schemas.user import User
from app.utils.auth import get_current_user
from db import db

router = APIRouter()


class SuccessResponse(BaseModel):
    success: bool
    score: Optional[int]


class UpdateCategory(BaseModel):
    completed: int
    categoryId: str
    proficiencyId: str


class UpdateQuiz(BaseModel):
    questionsCorrect: int
    quizId: str


class UpdateChallenge(BaseModel):
    dailyChallengeId: str
    evaluation: int


@router.put("/category", status_code=200, response_model=SuccessResponse)
async def update_user_category(
    data: UpdateCategory, current_user: User = Depends(get_current_user)
):
    try:
        score = data.completed * 30
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

        return SuccessResponse(success=True, score=score)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/quiz", status_code=200, response_model=SuccessResponse)
async def update_user_quiz(
    data: UpdateQuiz, current_user: User = Depends(get_current_user)
):
    try:
        score = data.questionsCorrect * 20
        await db.completedquiz.update_many(
            where={
                "AND": [
                    {"quizId": data.quizId},
                    {"userId": current_user.id},
                ]
            },
            data={"score": score},
        )

        return SuccessResponse(success=True, score=score)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/challenge", status_code=201, response_model=SuccessResponse)
async def update_user_challenge(
    data: UpdateChallenge, current_user: User = Depends(get_current_user)
):
    try:
        score = data.evaluation * 20
        await db.completedchallenge.create(
            data={
                "dailyChallengeId": data.dailyChallengeId,
                "score": score,
                "userId": current_user.id,
            },
        )

        return SuccessResponse(success=True, score=score)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
