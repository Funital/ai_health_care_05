from datetime import datetime

from sqlalchemy import Float, Integer, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from database.orm import Base


class User(Base):
    __tablename__ = "user"

    # 기본키 id 컬럼 
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # email 컬럼(중복 불가)
    email: Mapped[str] = mapped_column(
        String(256), unique=True
    )
    # 비밀번호 해시(암호화된 값)
    hashed_password: Mapped[str] = mapped_column(String(256))
    # 회원이 가입한 시각(DB에 저장된 시각을 자동 저장)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

class UserHealthProfile(Base):
    __tablename__ = "user_health_profile"

    # 기본키 id 컬럼 
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # user_id 컬럼(외래키)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)    # unique=True: 한 명의 회원이 하나의 건강 프로필만 가질 수 있도록 설정
    # 나이 컬럼
    age: Mapped[int] = mapped_column(Integer)
    # 키 컬럼
    height: Mapped[float] = mapped_column(Float)
    # 몸무게 컬럼
    weight: Mapped[float] = mapped_column(Float)
    # 흡연 여부 컬럼
    smoking: Mapped[bool] = mapped_column(Boolean)
    # 운동 횟수 컬럼(주당 운동 횟수)
    exercise_per_week: Mapped[int] = mapped_column(Integer)
    # 회원이 건강 프로필을 등록한 시각(DB에 저장된 시각을 자동 저장)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )