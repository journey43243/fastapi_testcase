from sqlalchemy import insert
from database.core import session_var
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from server.main import app
import pytest
from database.models import Base, ProductType
import asyncio
from httpx import AsyncClient
from typing import AsyncGenerator
from pydantic_settings import BaseSettings, SettingsConfigDict

pytest_plugins = ['pytester']


class Settings(BaseSettings):
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def DATABASE_URL(self):
        # DSN
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:" +\
            f"{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:" +\
            f"{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    model_config = SettingsConfigDict(env_file="test.env", extra="forbid")


settings = Settings()

test_engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
)

metadata = Base.metadata
metadata.bind = test_engine

async_session_maker = async_sessionmaker(test_engine, class_=AsyncSession,
                                         expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[session_var] = override_get_async_session


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():

    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
async def test_create_products_type():
    async with async_session_maker() as session:
        types = await session.execute(
            insert(ProductType).values([
                {"id": 1, "name": "trainers"},
                {"id": 2, "name": "jacket"},
                {"id": 3, "name": "socks"},
                {"id": 4, "name": "hats"}
            ]
            ))
        await session.commit()
        yield types


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
