from datetime import datetime
from operator import ge, lt
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

class UserHealthProfileCreateRequest(BaseModel):
    age: int = Field(...,ge=8, lt=150, example=30)
    height: float = Field(...,ge=1, lt=250, example=175.5)
    weight: float = Field(...,ge=1, lt=300, example=70.0)
    smoking: bool = Field(..., example=False)
    exercise_per_week: int = Field(...,ge=0, lt=8, example=3)

class UserHealthProfileResponse(BaseModel):
    id: int
    user_id: int
    age: int
    height: float
    weight: float
    smoking: bool
    exercise_per_week: int
    created_at: datetime