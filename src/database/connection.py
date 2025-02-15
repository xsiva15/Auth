from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from src.config import configuration
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .schemas import Base


async_engine: AsyncEngine = _create_async_engine(
    url=configuration.db.build_connection_str(),
    pool_pre_ping=True
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    await create_tables()

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()

        except Exception:
            # В случае ошибки откатываем все назад
            await session.rollback()
            raise

        finally:
            # В любом случае закрываю соединение
            await session.close()
