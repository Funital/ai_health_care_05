from enum import StrEnum
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from config import settings
from user.model import UserHealthProfile


client = AsyncOpenAI(api_key=settings.openai_api_key)

# enum: 선택 가능한 값들을 미리 선언
class ModelVersion(StrEnum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_5_MINI = "gpt-5-mini"

# 원하는 GPT 응답 형식
class RiskPredictionResultFormat(BaseModel):
    diabetes_probability: float = Field(..., description="0~1 사이의 당뇨 위험도")
    hypertension_probability: float = Field(..., description="0~1 사이의 고혈압 위험도") 
    summary: str = Field(..., description="결과에 대한 간단한 한 줄 설명")

# OpenAI 서버에 API 요청을 하고, 요청이 처리동안 대기 발생하는 I/O 작업
async def predict_health_risk(
    profile: UserHealthProfile, model_version: ModelVersion
) -> RiskPredictionResultFormat:
    prompt = f"""
    다음 건강 정보를 기반으로 당뇨와 고혈압 위험도를 0과 1 사이로 계산하라.

    age: {profile.age}
    height_cm: {profile.height_cm}
    weight_kg: {profile.weight_kg}
    smoking: {profile.smoking}
    exercise_per_week: {profile.exercise_per_week}
    """

    response = await client.responses.parse(
        model=str(model_version),
        input=prompt,
        text_format=RiskPredictionResultFormat
    )
    return response.output_parsed