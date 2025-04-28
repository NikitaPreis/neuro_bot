from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from bot.database.database import Base
from bot.settings import Settings

settings = Settings.load()


engine = create_async_engine(
    url=settings.db.db_url,
    future=True,
    echo=True,
    pool_pre_ping=True
)


AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)


async def get_db_session() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionFactory() as session:
        return session


async def init_models():
    """Create all models without alembic migrations."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
