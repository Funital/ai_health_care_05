from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select

from auth.jwt import verify_user
from database.connection import get_session
from user.model import UserHealthProfile

from prediction.model import HealthRiskPrediction
from prediction.llm import predict_health_risk
from prediction.schema import HealthRiskPredictRequest


router = APIRouter(prefix="/predictions", tags=["Prediction"])

@router.post(
    "",
    summary="당뇨/고혈압 위험도 예측 API",
    status_code=status.HTTP_201_CREATED,
)
async def predict_health_risk_handler(
    body: HealthRiskPredictRequest,
    user_id: int = Depends(verify_user),
    session = Depends(get_session),
):
    # 건강 프로필 조회
    stmt = (
        select(UserHealthProfile)
        .where(UserHealthProfile.user_id == user_id)
    )
    result = await session.execute(stmt)
    profile = result.scalar()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="건강 프로필이 존재하지 않습니다."
        )

    # ChatGPT API 요청
    result = await predict_health_risk(
        profile=profile, model_version=body.model_version
    )

    # DB에 저장
    new_prediction = HealthRiskPrediction(
        user_id=user_id,
        diabetes_probability=result.diabetes_probability,
        hypertension_probability=result.hypertension_probability,
        summary=result.summary,
        model_version=body.model_version
    )
    session.add(new_prediction)
    await session.commit()
    await session.refresh(new_prediction)

    return new_prediction