from pydantic import BaseModel, Field


class ChatSessionCreateRequest(BaseModel):
    prediction_id: int = Field(..., description="건강 위험도 예측 결과 ID")

class MessageRequest(BaseModel):
    content: str = Field(..., description="사용자 메시지 내용")