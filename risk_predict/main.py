from fastapi import FastAPI

from user import router as user_router
from prediction import router as prediction_router


app = FastAPI(
    title="건강 위험도 예측 서비스"
)

app.include_router(user_router.router)
app.include_router(prediction_router.router)