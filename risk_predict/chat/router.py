from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from auth.jwt import verify_user
from chat.schema import ChatSessionCreateRequest
from chat.model import HealthChatSession, HealthChatMessage, MessageRole
from chat.prompt import generate_default_system_prompt
from database.connection import get_session
from prediction.model import HealthRiskPrediction
from user.model import UserHealthProfile

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post(
    "/sessions",
    summary="채팅 세션 생성 API",
    status_code=status.HTTP_201_CREATED
)
async def create_chat_session_handler(
    body: ChatSessionCreateRequest,
    user_id: int = Depends(verify_user),
    session = Depends(get_session)
):
    # 예측 결과의 소유주가 맞는지 검증
    stmt = (
        select(HealthRiskPrediction).where(
            HealthRiskPrediction.id == body.prediction_id,
            HealthRiskPrediction.user_id == user_id
        )
    )
    result = await session.execute(stmt)
    prediction = result.scalar()
    if not prediction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")

    new_chat_session = HealthChatSession(
        user_id=user_id,
        health_risk_prediction_id=body.prediction_id,
        title=prediction.summary
    )
    session.add(new_chat_session)
    await session.commit()
    await session.refresh(new_chat_session)

    # 건강 프로필 조회
    stmt = (
        select(UserHealthProfile).where(
            UserHealthProfile.user_id == user_id
        )
    )
    result = await session.execute(stmt)
    user_profile = result.scalar()
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    # 기본 메시지 생성
    prompt = generate_default_system_prompt(
        profile=user_profile, 
        prediction=prediction
    )

    system_message = HealthChatMessage(
        session_id=new_chat_session.id,
        role=MessageRole.SYSTEM,
        content=prompt
    )
    session.add(system_message)
    await session.commit()
    await session.refresh(new_chat_session)

    return new_chat_session