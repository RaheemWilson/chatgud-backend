from fastapi import HTTPException
from typing import List
from pydantic import Depends
from app.utils.auth import get_current_user
from app.schemas.user import User

class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role.name not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
