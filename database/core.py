from .config import settings
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

engine_pg = create_async_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=15
)


session_var = async_sessionmaker(engine_pg, class_=AsyncSession,
                                 expire_on_commit=False)

metadata = MetaData()


def create_tables():
    metadata.create_all(engine_pg)
