from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///risk_predict.db"

# echo=True: SQLAlchemy가 실행하는 SQL 쿼리를 콘솔에 출력하도록 설정
async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

async def get_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()