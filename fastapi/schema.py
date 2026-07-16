import re   # Regular Expression
from pydantic import BaseModel, Field, field_validator, EmailStr

# 회원가입 요청에 사용되는 데이터 형식
class UserSignUpRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=32)

class UserUpdateRequest(BaseModel):
    username: str | None = Field(None, min_length=2, max_length=100)
    email: str | None = Field(None, email=True)

class UserResponse(BaseModel):

    id: int
    username: str = Field(..., min_length=2, max_length=100)
    email: str = Field(...)
