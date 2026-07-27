from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from auth.jwt import create_access_token, verify_user
from auth.password import hash_password, verify_password
from database.connection import get_session
from user.model import User, UserHealthProfile
from user.schema import UserSignUpRequest, UserResponse, UserLoginRequest, UserHealthProfileCreateRequest, UserHealthProfileResponse

# User 관련된 API 함수를 관리하는 객체
router = APIRouter(prefix="/user", tags=["User"])

@router.post(
    "",
    summary="회원가입 API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def signup_user_handler(
    body: UserSignUpRequest,
    session = Depends(get_session)
):
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    existing_user = result.scalar()
    if existing_user:
        raise HTTPException(status_code=409, detail="이미 존재하는 사용자입니다.")

    # 비밀번호 해싱
    hashed_password = hash_password(plain_password=body.password)

    new_user = User(
        email=body.email,
        hashed_password=hashed_password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post(
    "/login",
    summary="로그인 API",
    status_code=status.HTTP_200_OK,
)
async def login_user_handler(
    body: UserLoginRequest,
    session = Depends(get_session)
):
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    existing_user = result.scalar()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일과 비밀번호가 일치하지 않습니다.")

    is_verified = verify_password(
        plain_password=body.password,
        hashed_password=existing_user.hashed_password
    )

    if not is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일과 비밀번호가 일치하지 않습니다.")

    # JWT 발급
    access_token = create_access_token(user_id=existing_user.id)

    return {"message": "로그인 성공", "access_token": access_token}

from fastapi import Header

@router.get(
    "/me",
    summary="내 정보 조회 API",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_me_handler(
    user_id = Depends(verify_user),
    session = Depends(get_session)
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()
    return user

@router.post(
    "/health-profiles",
    summary="건강 프로필 생성 API",
    response_model=UserHealthProfileResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_health_profile_handler(
    body: UserHealthProfileCreateRequest,
    user_id: int = Depends(verify_user),
    session = Depends(get_session)
):
    stmt = select(UserHealthProfile).where(UserHealthProfile.user_id == user_id)
    result = await session.execute(stmt)
    existing_profile = result.scalar()
    if existing_profile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 건강 프로필이 존재합니다.")
    # 새로운 건강 프로필 생성
    profile_data = body.model_dump()  # Pydantic 모델을 딕셔너리로 변환

    new_profile = UserHealthProfile(
        user_id=user_id,
        **profile_data
    )
    session.add(new_profile)
    await session.commit()  
    await session.refresh(new_profile)
    return new_profile