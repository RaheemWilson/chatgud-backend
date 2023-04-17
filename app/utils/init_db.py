from db import db
from files.parse_files import parse_file
import pandas as pd

async def init_db():
    #Create proficiency levels
    levels = parse_file("files/proficiency_.csv")
    
    
    db_levels = await db.proficiency.find_many()
    
    if len(db_levels) > 0:
        for level in levels:
            is_level_in_db = await db.proficiency.find_first(
                where={
                    'name': level['name']
                }
            )
            
            if not is_level_in_db:
                await db.proficiency.create(data=level)
    else:
        await db.proficiency.create_many(data=levels)
        
        
    #Create categories
    categories = parse_file("files/categories_.csv")
    
    
    db_categories = await db.category.find_many()
    
    if len(db_categories) > 0:
        for category in categories:
            is_category_in_db = await db.category.find_first(
                where={
                    'name': category['name']
                }
            )
            
            if not is_category_in_db:
                await db.category.create(data=category)
    else:
        await db.category.create_many(data=categories)
        
    #Create resources
    resources = parse_file("files/resources.csv")
    
    db_resources = await db.resource.find_many()
    
    if len(db_resources) > 0:
        for resource in resources:
            is_resource_in_db = await db.resource.find_first(
                where={
                    'name': resource['name']
                }
            )
            
            if not is_resource_in_db:
                await db.resource.create(data=resource)
    else:
        await db.resource.create_many(data=resources)
        
        
    #Create task choice
    taskchoices = parse_file("files/taskchoice.csv")
    
    df = pd.read_csv('files/taskchoice.csv')

    taskchoices = df.groupby('id')['choice'].agg(list).to_dict()
    
    for taskchoice in taskchoices:
        is_taskchoice_in_db = await db.taskchoice.find_first(
            where={
                'id': taskchoice
            }
        )
        
        if not is_taskchoice_in_db:
            await db.taskchoice.create(data={
                "id": taskchoice,
                "choices": {
                    'connect': [{ 'id': id } for id in taskchoices[taskchoice]]
                }
            })
            
    #Create task choice
    tasks = parse_file("files/task.csv")      
    
    for task in tasks:
        is_task_in_db = await db.task.find_first(
            where={
                'id': task['id']
            }
        )
        
        if not is_task_in_db:
            await db.task.create(data=task)
            
    #Create quiz
    quizzes = parse_file("files/quiz.csv")      
    
    for quiz in quizzes:
        is_quiz_in_db = await db.quiz.find_first(
            where={
                'id': quiz['id']
            }
        )
        
        if not is_quiz_in_db:
            await db.quiz.create(data=quiz)
            
    #Create quiz
    questions = parse_file("files/quiz-questions.csv")   
    
    for question in questions:
        is_question_in_db = await db.quizquestion.find_first(
            where={
                'id': question['id']
            }
        )
        
        if not is_question_in_db:
            await db.quizquestion.create(data=question)
            
    