from fastapi import Depends, status, HTTPException
from sqlalchemy import select

from chat.model import HealthChatMessage, HealthChatSession
from chat.prompt import generate_default_system_prompt
from database.connection import get_session
from prediction.model import HealthRiskPrediction
from user.model import UserHealthProfile

class ChatRepository:
    def __init__(self, session = Depends(get_session)):
        self.session = session

    async def verify_prediction(self, prediction_id: int, user_id: int) -> HealthRiskPrediction:
        # 예측 결과의 소유주가 맞는지 검증
        stmt = (
            select(HealthRiskPrediction).where(
                HealthRiskPrediction.id == prediction_id,
                HealthRiskPrediction.user_id == user_id
            )
        )
        result = await self.session.execute(stmt)
        prediction = result.scalar()
        if not prediction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")

        return prediction

    async def get_user_health_profile(self, user_id: int):
        # 건강 프로필 조회
        stmt = (
            select(UserHealthProfile).where(
                UserHealthProfile.user_id == user_id
            )
        )
        result = await self.session.execute(stmt)
        user_profile = result.scalar()
        if not user_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

        return user_profile

    async def create_chat_session(self, user_id: int, prediction: HealthRiskPrediction, profile: UserHealthProfile) -> HealthChatSession:
        new_chat_session = HealthChatSession(
            user_id=user_id,
            health_risk_prediction_id=body.prediction_id,
            title=prediction.summary
        )
    
        self.session.add(new_chat_session)
        await self.session.commit()
        await self.session.refresh(new_chat_session)

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
        self.session.add(system_message)
        await self.session.commit()
        await self.session.refresh(new_chat_session)
    