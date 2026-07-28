from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# request
class UserSignUpRequest(BaseModel):
    email: EmailStr = Field(..., examples=["alex@fastapi.com"])
    password: str = Field(..., min_length=4, examples=["password123"])

class UserLogInRequest(BaseModel):
    email: EmailStr = Field(..., examples=["alex@fastapi.com"])
    password: str = Field(..., min_length=4, examples=["password123"])

class UserHealthProfileCreateRequest(BaseModel):
    age: int = Field(..., ge=8, lt=150)
    height_cm: float = Field(..., ge=1, lt=250)
    weight_kg: float = Field(..., ge=1, lt=300)
    smoking: bool
    exercise_per_week: int = Field(..., ge=0, lt=8)


# response
class UserHealthProfileResponse(BaseModel):
    id: int
    user_id: int
    age: int
    height_cm: float
    weight_kg: float
    smoking: bool
    exercise_per_week: int
    created_at: datetime

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    health_profile: UserHealthProfileResponse | None

    # 객체를 읽을 때, 속성 읽기(.attr) 허용
    model_config = ConfigDict(from_attributes=True)