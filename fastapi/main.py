from sqlalchemy import select

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query

from connection import SessionFactory, get_session
from models import User
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest

app = FastAPI()

# users: list[dict[str, int | str]] = [
#     {"id": 1, "username": "user1", "email": "user1@example.com", "password": "password1"},
#     {"id": 2, "username": "user2", "email": "user2@example.com", "password": "password2"},
#     {"id": 3, "username": "user3", "email": "user3@example.com", "password": "password3"}
# ]

@app.get(
    "/users",
    summary="전체 사용자 조회 api",
    response_model=list[UserResponse],
    status_code=200
)
# def get_all_users_handler():
#     stmt = select(User)
#     with SessionFactory() as session:   # 자동 close
#         users = session.execute(stmt).scalars().all()
#         return users
def get_all_users_handler(
    session = Depends(get_session),
):
    stmt = select(User)
    result = session.execute(stmt)
    users: list[User] = result.scalars().all()
    return users

@app.get(
    "/users/search",
    summary="사용자 검색 api",
    response_model=list[UserResponse]
)
def search_users_handler(
    name: str | None = Query(None),
    session = Depends(get_session)
):
    if name is None:
        return []

    stmt = select(User).where(User.username.contains(name))
    result = session.execute(stmt)
    users: list[User] = result.scalars().all()
    return users
    # with SessionFactory() as session:   # 자동 close
    #     users = session.execute(stmt).scalars().all()
    #     return users

@app.get(
    "/users/{user_id}",
    summary="사용자 조회 api",
    response_model=UserResponse,
    status_code=200
)
def get_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_session)
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user: User | None = result.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

    
@app.post(
    "/users",
    summary="회원가입 api",
    response_model=UserResponse,
    status_code=201
)
def user_signup_handler(
    body: UserSignUpRequest,
    session = Depends(get_session)
):
    new_user = User(username=body.username, email=body.email, password=body.password)

    session.add(new_user)
    session.commit()
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
    session = Depends(get_session)
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user: User | None = result.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if body.username is not None:
        user.username = body.username
    if body.email is not None:
        user.email = body.email
    session.commit()
    return user

@app.delete(
    "/users/{user_id}",
    summary="사용자 삭제 api",
    response_model=None,
    status_code=204
)
def delete_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_session)
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user: User | None = result.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    session.delete(user)
    session.commit()