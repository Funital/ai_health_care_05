from fastapi import APIRouter, Depends, status

from auth.jwt import verify_user
from database.connection import get_session

router = APIRouter(prefix="/prediction", tags=["Prediction"])

@router.post(
    "",
    summary="건강 위험도 예측 API",
    status_code=status.HTTP_201_CREATED,
)
async def predict_health_risk_handler(
    user_id: int = Depends(verify_user),
    session = Depends(get_session)
):
    return