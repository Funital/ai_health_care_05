from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserSignUpRequest(BaseModel):
    email: EmailStr = Field(..., example="alex@example.com")
    password: str = Field(..., min_length=4, example="password1234")

class UserSignUpResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., example="alex@example.com")
    password: str = Field(..., min_length=4, example="password1234")