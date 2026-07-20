import re   # Regular Expression
from pydantic import BaseModel, Field, field_validator

# 회원가입 요청에 사용되는 데이터 형식
class UserSignUpRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    email: str = Field(...)
    password: str = Field(..., min_length=8, max_length=32)

class UserUpdateRequest(BaseModel):
    username: str | None = Field(None, min_length=2, max_length=100)
    email: str | None = None

class UserResponse(BaseModel):

    id: int
    username: str = Field(..., min_length=2, max_length=100)
    email: str = Field(...)

class UserInputRequest(BaseModel):
    user_input: str
