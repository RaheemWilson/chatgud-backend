from typing import List, Optional
from pydantic import BaseModel

from app.schemas.category import Category
from app.schemas.proficiency import Proficiency
from app.schemas.resource import Resource

class TaskChoice(BaseModel):
    id: str
    choices: List[Resource]

class Task(BaseModel):
    id: str
    problem: str
    category: Optional[Category]
    proficiency: Optional[Proficiency]
    answerId: str
    answer: Resource
    categoryId: str
    proficiencyId: str
    options: str
    type: str
    taskOrder: int
    taskChoice: TaskChoice

class QuizQuestion(BaseModel):
    id: str
    task: Task
    quizId: str
    taskId: str
    questionOrder: int
    questionResource: Optional[Resource]
    questionResourceId: Optional[str]

class Quiz(BaseModel):
    id: str
    category: Optional[Category]
    categoryId: str
    proficiency: Optional[Proficiency]
    proficiencyId: str
    quizQuestion: List[QuizQuestion]


    
        
    