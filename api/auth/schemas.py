from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
import re

class UserRegister(BaseModel):
    username: str = Field(..., min_length=5, max_length=35, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr = Field(..., min_length=5, max_length=256)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
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
    
class UserLogin(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=256)
    password: str = Field(..., min_length=8, max_length=128)
    
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)
    
class TokenResponse(BaseModel):
    success: bool
    message: str
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Optional[str]