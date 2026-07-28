from enum import StrEnum

from database.orm import Base

from sqlalchemy import Integer, ForeignKey, String, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

# 대화 구분 단위
class HealthChatSession(Base):
    __tablename__ = "health_chat_session"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # 채팅 세션 소유한 소유지
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # 채팅 세션 생성하는데 기반이 된 예측 결과
    health_risk_prediction_id: Mapped[int] = mapped_column(
        ForeignKey("health_risk_prediction.id")
    )
    # 채팅 세션의 제목
    title: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

# 채팅 세션 안에서 실제로 발생하는 메시지
class HealthChatMessage(Base):
    __tablename__ = "health_chat_message"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # 메시지가 속한 채팅 세션
    session_id: Mapped[int] = mapped_column(
        ForeignKey("health_chat_session.id")
    )
    # 어떤 종류의 프롬프트인지(system/user/assistant)
    role: Mapped[MessageRole] = mapped_column(String(10))
    # 메시지 내용
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )