from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


_db_available: bool = False


async def get_db() -> AsyncSession | None:
    """Yield a DB session, or None if PostgreSQL is not reachable.

    The yield-None path is unconditional (not inside an except block),
    which is required for Python 3.14 generator semantics.
    """
    if not _db_available:
        yield None
        return
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables() -> None:
    global _db_available
    import logging
    logger = logging.getLogger(__name__)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        _db_available = True
        logger.info("PostgreSQL connected — DB persistence enabled.")
    except Exception as exc:
        logger.warning(
            "PostgreSQL not reachable — running without DB persistence. (%s)", exc
        )
