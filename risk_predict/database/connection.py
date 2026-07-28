from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///risk_predict.db"

# echo=True -> SQLAlchemy에서 발생하는 SQL 쿼리를 출력
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