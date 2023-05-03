from typing import List
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, status
from app.schemas.user import UpdateUser, User, UserOverview, Users
from fastapi.responses import JSONResponse

from app.utils.auth import get_current_user
from db import db


router = APIRouter()


@router.put("/user", response_model=User, status_code=200)
async def update_user(
    updates: UpdateUser, current_user: User = Depends(get_current_user)
):
    try:
        updated_user = await db.user.update(
            where={"id": current_user.id},
            data=updates.dict(),
            include={"proficiency": True},
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/user/quizzes", status_code=200)
async def get_user_quizzes(current_user: User = Depends(get_current_user)):
    try:
        user_quizzes = await db.completedquiz.find_many(
            where={"userId": current_user.id},
            include={"quiz": {"include": {"category": True}}},
        )
        return user_quizzes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/user/overview", response_model=UserOverview, status_code=200)
async def get_user_overview(current_user: User = Depends(get_current_user)):
    try:
        user_quizzes = await db.completedquiz.find_many(
            where={"AND": [{"userId": current_user.id}, {"score": {"gt": 0}}]},
        )
        # print(type user_quizzes, 'type')
        user_cat = await db.completedcategory.find_many(
            where={"AND": [{"userId": current_user.id}, {"score": {"gt": 0}}]},
        )
        user_chal = await db.completedchallenge.find_many(
            where={"AND": [{"userId": current_user.id}, {"score": {"gt": 0}}]},
        )

        user_quizzes_score = sum([quiz.score for quiz in user_quizzes])
        user_cat_score = sum([cat.score for cat in user_cat])
        user_chal_score = sum([chal.score for chal in user_chal])

        score_details = {
            "score": user_cat_score + user_chal_score + user_quizzes_score,
            "completedQuiz": len(user_quizzes),
            "completedChallenges": len(user_chal),
            "completedCategories": len(user_cat),
            "quizScore": user_quizzes_score,
            "challengeScore": user_chal_score,
            "categoryScore": user_cat_score,
        }

        return UserOverview(**score_details)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
  
    
@router.get("/users/leaderboard", response_model=List[Users], status_code=200)
async def get_user_overview(current_user: User = Depends(get_current_user)):
    try:
        users = []
        
        db_users = await db.user.find_many()
        
        for user in db_users:
            user_quizzes = await db.completedquiz.find_many(
                where={"AND": [{"userId": user.id}, {"score": {"gt": 0}}]},
            )
            # print(type user_quizzes, 'type')
            user_cat = await db.completedcategory.find_many(
                where={"AND": [{"userId": user.id}, {"score": {"gt": 0}}]},
            )
            user_chal = await db.completedchallenge.find_many(
                where={"AND": [{"userId": user.id}, {"score": {"gt": 0}}]},
            )

            user_quizzes_score = sum([quiz.score for quiz in user_quizzes])
            user_cat_score = sum([cat.score for cat in user_cat])
            user_chal_score = sum([chal.score for chal in user_chal])
            
            user_detail = {
                "id": user.id,
                "score": user_cat_score + user_chal_score + user_quizzes_score,
                "username": user.username
            }
            
            users += [user_detail]

        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
    

