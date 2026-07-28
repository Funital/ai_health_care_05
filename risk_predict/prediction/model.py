from datetime import datetime

from sqlalchemy import Integer, ForeignKey, Float, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database.orm import Base


# 당뇨/고혈압 위험도 예측 결과
class HealthRiskPrediction(Base):
    __tablename__ = "health_risk_prediction"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # 사용자:예측결과 -> 1:N 관계
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    diabetes_probability: Mapped[float] = mapped_column(Float)
    hypertension_probability: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str] = mapped_column(String(50))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )