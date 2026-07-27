from database.orm import Base

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class HealthRiskPrediction(Base):
    __tablename__ = "health_risk_predictions"

    id = Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    diabetes_probability: Mapped[float] = mapped_column(Float)
    hypertension_probability: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str] = mapped_column(String(50))