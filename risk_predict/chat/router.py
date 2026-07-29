from fastapi import APIRouter, status, Depends, HTTPException, Path
from fastapi.responses import StreamingResponse
from sqlalchemy import select

from auth.jwt import verify_user
from chat.schema import ChatSessionCreateRequest, MessageRequest
from chat.model import HealthChatSession, HealthChatMessage, MessageRole
from chat.prompt import generate_default_system_prompt
from chat.repository import ChatRepository
from database.connection import get_session
from prediction.model import HealthRiskPrediction
from user.model import UserHealthProfile
from llm import client, ModelVersion


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

@router.post(
    "/sessions//{session_id}/messages",
    summary="대화 세션에 새로운 메시지를 추가하는 API",
    status_code=status.HTTP_201_CREATED,
)
async def create_chat_message_handler(
    body: MessageRequest,
    session_id: int = Path(..., ge=1),
    user_id: int = Depends(verify_user),
    session = Depends(get_session),
):
    stmt = (
        select(HealthChatSession)
        .where(
            HealthChatSession.id == session_id,
            HealthChatSession.user_id == user_id
        )
    )
    result = await session.execute(stmt)
    chat_session = result.scalar()
    if not chat_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 대화 세션입니다.",
        )

    user_message = HealthChatMessage(
        session_id=session_id,
        role=MessageRole.USER,
        content=body.content
    )
    session.add(user_message)
    await session.commit()

    result = await session.execute(
        select(HealthChatMessage)
        .where(HealthChatMessage.session_id == chat_session.id)
        .order_by(HealthChatMessage.id.desc())
        .limit(10)  # 최근 10개의 메시지만 가져오기
    )

    chat_messages = result.scalars().all()
    chat_messages.reverse()  # 최근 메시지가 마지막에 오도록 순서 변경
    messages =  [
        {
            "role": m.role,
            "content": m.content
        }
        for m in chat_messages
    ]

    async def token_generator():
        stream = await client.response.create(
            model=str(ModelVersion.GPT_4O_MINI),
            input=messages,
            stream=True
        )

        assistant_content = ""

        async for event in stream:
            if event.type == "response.output_text.delta":
                token = event.delta
                assistant_content += token
                yield token

        assistant_message = HealthChatMessage(
            session_id=session_id,
            role=MessageRole.ASSISTANT,
            content=assistant_content
        )

        session.add(assistant_message)
        await session.commit()

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream"
    )