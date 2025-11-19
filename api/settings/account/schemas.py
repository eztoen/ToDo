import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

class ChangeName(BaseModel):
    username: str = Field(..., min_length=5, max_length=35, pattern=r'^[a-zA-Z0-9_]+$')

class ChangeEmail(BaseModel):
    email: EmailStr
    
class ChangePassword(BaseModel):
    actual_password: str = Field(..., min_length=8, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator("new_password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        if " " in value:
            raise ValueError("Password cannot contain spaces.")
        return value
    
class DeleteAccount(BaseModel):
    confirmation_message: Literal['DELETE MY ACCOUNT']