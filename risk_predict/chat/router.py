from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from auth.jwt import verify_user
from chat.repository import ChatRepository
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
    repository: ChatRepository = Depends(ChatRepository),
):
    prediction = await repository.verify_prediction(body.prediction_id, user_id)

    

    user_profile = await repository.get_user_health_profile(user_id)

   

    return new_chat_session