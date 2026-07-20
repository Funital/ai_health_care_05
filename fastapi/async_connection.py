# 데이터베이스에 요청을 하기 위한 연결 정보를 관리
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///./example.db"  # SQLite 비동기 드라이버

async_engine = create_async_engine(DATABASE_URL, echo=True)

# 실제 요청을 보내는 단위
AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    autocommit=False,       # 메모리 상의 데이터를 다루는 방식
    autoflush=False,
    expire_on_commit=False
)

# session 관리 의존성 함수
async def get_async_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()