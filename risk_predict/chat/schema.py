from pydantic import BaseModel, Field


class ChatSessionCreateRequest(BaseModel):
    prediction_id: int = Field(..., description="건강 위험도 예측 결과 ID")