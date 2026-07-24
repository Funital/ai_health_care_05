import jwt  # pyjwt 라이브러리
from datetime import datetime, timezone, timedelta
from config import settings

from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBearer

def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),  # subject: 토큰의 주체
        "exp": datetime.now(timezone.utc) +timedelta(hours=24)  # expiration time: 토큰 만료 시간 설정
    }

    return jwt.encode(
        payload = payload,
        key = settings.jwt_secret_key,
        algorithm = "HS256"
    )

def verify_access_token(access_token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt = access_token,
            key = settings.jwt_secret_key,
            algorithms = ["HS256"]
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 토큰 형식입니다."
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다."
        )
    return payload

http_bearer = HTTPBearer()

def verify_user(
    auth_header = Depends(http_bearer)
) -> int:
    access_token = auth_header.credentials
    payload = verify_access_token(access_token=access_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="sub 값이 없습니다."
        )
    return int(user_id)