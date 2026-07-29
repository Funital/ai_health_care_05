from pydantic import BaseModel

from llm import ModelVersion


# request
# 건강 위험도 예측 API 요청 본문 형식
class HealthRiskPredictRequest(BaseModel):
    model_version: ModelVersion