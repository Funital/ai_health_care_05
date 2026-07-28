from fastapi import Depends, status, HTTPException
from sqlalchemy import select

from database.connection import get_session
from chat.model import HealthChatSession, HealthChatMessage, MessageRole
from chat.prompt import generate_default_system_prompt
from prediction.model import HealthRiskPrediction
from user.model import UserHealthProfile


class ChatRepository:
    def __init__(self, session = Depends(get_session)):
        self.session = session

    # 예측 결과(prediction)의 소유주 검증
    async def verify_prediction(
        self, prediction_id: int, user_id: int
    ) -> HealthRiskPrediction:
        stmt = (
            select(HealthRiskPrediction)
            .where(
                HealthRiskPrediction.id == prediction_id,
                HealthRiskPrediction.user_id == user_id
            )
        )
        result = await self.session.execute(stmt)
        prediction = result.scalar()
        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 예측 결과입니다.",
            )
        return prediction

    async def get_user_health_profile(self, user_id: int) -> UserHealthProfile:
        # 건강 프로필 조회 
        stmt = (
            select(UserHealthProfile)
            .where(UserHealthProfile.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        user_profile = result.scalar()
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자 건강 프로필이 존재하지 않습니다."
            )
        return user_profile

    async def create_chat_session(
        self, 
        user_id: int, 
        prediction: HealthRiskPrediction, 
        profile: UserHealthProfile
    ) -> HealthChatSession:
        # 새로운 대화 세션 생성
        new_chat_session = HealthChatSession(
            user_id=user_id,
            health_risk_prediction_id=prediction.id,
            title=prediction.summary
        )
        self.session.add(new_chat_session)
        await self.session.flush()  # 임시 저장
    
        # 기본 메시지 생성
        prompt = generate_default_system_prompt(
            profile=profile,
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
        
        return new_chat_session