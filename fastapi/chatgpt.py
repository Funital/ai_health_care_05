from openai import OpenAI
from pydantic import BaseModel, Field
from config import settings

client = OpenAI(api_key=settings.openai_api_key)

user_input = input("질문을 입력하세요: ")

class ResponseFormat(BaseModel):
    result: str = Field(description="최종 답변")
    confidence: int = Field(description="답변 신뢰도")

response = client.responses.parse(
    model="gpt-4o-mini",
    input=user_input,
    text_format=ResponseFormat
)



print(response.output_parsed)

# class NutrionResponse(BaseModel):
#     calories: int = Field(description="칼로리")
#     protein: float = Field(description="단백질 (g)")
#     fat: float = Field(description="지방 (g)")
#     carbohydrates: float = Field(description="탄수화물 (g)")