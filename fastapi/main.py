from fastapi import Body, FastAPI, HTTPException, Path, Query

from connection import SessionFactory
from models import User
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest

app = FastAPI()

# (...): 필수값이다.
# ("default"): 기본값을 설정한다.

# # query parameters
# @app.get("/users/search", summary="회원 검색 api")
# def search_user_handler(name: str = Query("default", min_length=2, max_length=100)):  
#     return {"name": name}

# # path parameters
# @app.get("/user/{user_id}", summary="회원 조회 api")
# def get_user_handler(user_id: int = Path(..., ge=1)):
#     return {"user_id": user_id}

# # @app.get("/items/{item_name}")
# # def get_item_handler(item_name: str = Path(..., min_length=3, max_length=6)):
# #     return {"item_name": item_name}

# @app.get("/items/search", summary="상품 검색 api")
# def search_item_handler(
#     q: str = Query(...),
#     limit: int = Query(10)
#     ):
#     return {"q": q, "limit": limit}

# @app.post(
#     "/users",
#     summary="Create a user",
#     response_model=UserResponse
# )
# def signup_user_handler(
#     body: UserSignUpRequest
# ):
#     new_user = {
#         "id": 1,
#         "username": body.username,
#         "email": body.email
#     }
#     return UserResponse(**new_user)

# ---------------------------------------------

users: list[dict[str, int | str]] = [
    {"id": 1, "username": "user1", "email": "user1@example.com", "password": "password1"},
    {"id": 2, "username": "user2", "email": "user2@example.com", "password": "password2"},
    {"id": 3, "username": "user3", "email": "user3@example.com", "password": "password3"}
]

@app.get(
    "/users",
    summary="전체 사용자 조회 api",
    response_model=list[UserResponse],
    status_code=200
)
def get_all_users_handler():
    session = SessionFactory()
    users = session.query(User).all()
    return users

@app.get(
    "/users/{user_id}",
    summary="사용자 조회 api",
    response_model=UserResponse,
    status_code=200
)
def get_user_handler(user_id: int = Path(..., ge=1)):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get(
    "/users/search",
    summary="사용자 검색 api",
    response_model=list[UserResponse]
)
def search_users_handler(
    name: str | None = Query(None)
):
    result = []
    if name is None:
        return result
    
    for user in users:
        if name in user["username"]:
            result.append(user)
    return result

@app.post(
    "/users",
    summary="회원가입 api",
    response_model=UserResponse,
    status_code=201
)
def user_signup_handler(
    body: UserSignUpRequest
):
    new_user = User(username=body.username, email=body.email, password=body.password)

    session = SessionFactory()
    session.add(new_user)
    session.commit()
    session.close()
    return new_user

@app.patch(
    "/users/{user_id}",
    summary="사용자 정보 수정 api",
    response_model=UserResponse,
    status_code=200
)
def update_user_handler(
    user_id: int = Path(..., ge=1),
    body: UserUpdateRequest = Body(...),
):
    for user in users:
        if user["id"] == user_id:
            if body.username is not None:
                user["username"] = body.username
            if body.email is not None:
                user["email"] = body.email
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete(
    "/users/{user_id}",
    summary="사용자 삭제 api",
    response_model=None,
    status_code=204
)
def delete_user_handler(
    user_id: int = Path(..., ge=1)
):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return
    raise HTTPException(status_code=404, detail="User not found")