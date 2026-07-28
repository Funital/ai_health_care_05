from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey, Float, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    health_profile = relationship(
        "UserHealthProfile",
        uselist=False,  # 일대일 관계
        lazy="joined",  # User를 조회할 때, JOIN으로 HealthProfile 함께 조회
    )


class UserHealthProfile(Base):
    __tablename__ = "user_health_profile"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # 프로필의 소유주(user)를 나타내는 외래키(FK) - 일대일 관계(unique)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)

    age: Mapped[int] = mapped_column(Integer)
    height_cm: Mapped[float] = mapped_column(Float)
    weight_kg: Mapped[float] = mapped_column(Float)
    smoking: Mapped[bool] = mapped_column(Boolean)
    exercise_per_week: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now() 
    )