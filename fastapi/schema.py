import re   # Regular Expression
from pydantic import BaseModel, Field, field_validator, EmailStr

# 회원가입 요청에 사용되는 데이터 형식
class UserSignUpRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., email=True)

class UserUpdateRequest(BaseModel):
    username: str | None = Field(None, min_length=2, max_length=100)
    email: str | None = Field(None, email=True)

class UserResponse(BaseModel):
    id: int
    username: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., email=True)
