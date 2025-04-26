from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from constants import DB_URL
from database.models import category, spec

__engine = create_async_engine(
    DB_URL,
    pool_size=5,
    max_overflow=10,  # max_overflow + pool_size = max size = 15
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,  # Phát hiện và loại bỏ kết nối chết
)

__session_maker = async_sessionmaker(__engine)


async def aget_session():
    session = __session_maker()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.aclose()
