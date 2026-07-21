from contextlib import asynccontextmanager

import anyio
from llama_cpp import Llama
from sqlalchemy import select
from openai import AsyncOpenAI
from config import settings

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import StreamingResponse

from async_connection import get_async_session
from models import User
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest, UserInputRequest

@asynccontextmanager
async def lifespan(app):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100

    app.state.llm = Llama(
        model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
        n_ctx=4096,
        n_threads=2,
        verbose=False,   # 로그 찍기
        chat_format="llama-3",
    )

    app.state.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    yield

app = FastAPI(lifespan=lifespan)

@app.get(
    "/users",
    summary="전체 사용자 조회 api",
    response_model=list[UserResponse],
    status_code=200
)
async def get_all_users_handler(
    session = Depends(get_async_session),
):
    stmt = select(User)
    result = await session.execute(stmt)
    users: list[User] = result.scalars().all()
    return users

@app.get(
    "/users/search",
    summary="사용자 검색 api",
    response_model=list[UserResponse]
)
async def search_users_handler(
    name: str | None = Query(None),
    session = Depends(get_async_session)
):
    if name is None:
        return []

    stmt = select(User).where(User.username.contains(name))
    result = await session.execute(stmt)
    users: list[User] = result.scalars().all()
    return users

@app.get(
    "/users/{user_id}",
    summary="사용자 조회 api",
    response_model=UserResponse,
    status_code=200
)
async def get_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_async_session)
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user: User | None = result.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post(
    "/users",
    summary="회원가입 api",
    response_model=UserResponse,
    status_code=201
)
async def user_signup_handler(
    body: UserSignUpRequest,
    session = Depends(get_async_session)
):
    new_user = User(username=body.username, email=body.email, password=body.password)
    session.add(new_user)
    await session.commit()
    return new_user

@app.patch(
    "/users/{user_id}",
    summary="사용자 정보 수정 api",
    response_model=UserResponse,
    status_code=200
)
async def update_user_handler(
    user_id: int = Path(..., ge=1),
    body: UserUpdateRequest = Body(...),
    session = Depends(get_async_session)
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user: User | None = result.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if body.username is not None:
        user.username = body.username
    if body.email is not None:
        user.email = body.email
    await session.commit()
    return user

@app.delete(
    "/users/{user_id}",
    summary="사용자 삭제 api",
    response_model=None,
    status_code=204
)
async def delete_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_async_session)
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user: User | None = result.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

def get_llm(request: Request):
    return request.app.state.llm

@app.post("/chats")
async def create_chat_handler(
    # request: Request,   # Request 객체를 통해 FastAPI의 상태에 접근
    body: UserInputRequest, # 요청 본문
    llm = Depends(get_llm)
    # session = Depends(get_async_session)
):
    SYSTEM_PROMPT = (
        "You are a concise assistant. "
        "Always reply in the same language as the user's input. "
        "Do not change the language. "
        "Do not mix languages."
    )
    # 채팅 생성 로직 구현
    # llm = get_llm(request)  # FastAPI의 상태에서 Llama 인스턴스를 가져옴
    
    # answer = response["choices"][0]["message"]["content"]

    # 토큰이 생성될 때마다 토큰을 반환하는 함수
    def token_generator():
        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": body.user_input
                }
            ],
            max_tokens=256,
            temperature=0.7,
            stream=True # 스트리밍 방식으로 토큰 단위로 반환
        )
        for chunk in response:
            token = chunk["choices"][0]["delta"].get("content")
            if token:
                yield token

    return StreamingResponse(
        # 제너레이터 객체 -> 여러 개의 데이터를 만들어주는 객체
        token_generator(),
        media_type="text/event-stream",
    )

@app.post("/chat-gpt")
async def chat_gpt_handler(
    request: Request,
    body: UserInputRequest
):
    client = request.app.state.openai_client

    async def stream_generator():
        async with client.responses.stream(
            model="gpt-4o-mini",
            input=body.user_input,
        ) as stream:
            async for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta   # 토큰 반환
                elif event.type == "response.completed":
                    break

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream"
    )
    # response = await client.responses.create(
    #     model="gpt-4o-mini",
    #     input=body.user_input,
    # )
    # return {"answer": response.output_text}