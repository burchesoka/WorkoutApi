from databases import Database

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings


engine = create_async_engine(
    f'postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@'
    f'{settings.db_host}:5432/{settings.db_name}',
    echo=True,
    future=True
)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


database = Database(
    f'postgresql://{settings.db_user}:{settings.db_pass}@'
    f'{settings.db_host}:5432/{settings.db_name}',
)
