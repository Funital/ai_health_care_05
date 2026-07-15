# 데이터베이스에 요청을 하기 위한 연결 정보를 관리

# let vs const
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./example.db"  # SQLite 데이터베이스 URL

engine = create_engine(DATABASE_URL, echo=True)

# 실제 요청을 보내는 단위
SessionFactory = sessionmaker(
    bind=engine,
    autocommit=False,       # 메모리 상의 데이터를 다루는 방식
    autoflush=False,
    expire_on_commit=False
)