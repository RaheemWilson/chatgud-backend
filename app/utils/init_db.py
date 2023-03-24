from db import db
from files.parse_files import parse_file


async def init_db():
    #Create proficiency levels
    levels = parse_file("files/proficiency.csv")
    
    
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
    categories = parse_file("files/categories.csv")
    
    
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
        