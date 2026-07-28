from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select

from auth.jwt import verify_user
from chat.schema import ChatSessionCreateRequest
from chat.model import HealthChatSession, HealthChatMessage, MessageRole
from chat.prompt import generate_default_system_prompt
from chat.repository import ChatRepository
from database.connection import get_session
from prediction.model import HealthRiskPrediction
from user.model import UserHealthProfile


router = APIRouter(prefix="/chats", tags=["Chat"])

@router.post(
    "/sessions",
    summary="새로운 대화 세션을 생성하는 API",
    status_code=status.HTTP_201_CREATED,
)
async def create_chat_session_handler(
    body: ChatSessionCreateRequest,
    user_id: int = Depends(verify_user),
    repository: ChatRepository = Depends(),
):
    prediction = await repository.verify_prediction(
        prediction_id=body.prediction_id, user_id=user_id
    )
    profile = await repository.get_user_health_profile(user_id=user_id)
    new_chat_session = await repository.create_chat_session(
        user_id=user_id, prediction=prediction, profile=profile
    )
    return new_chat_session