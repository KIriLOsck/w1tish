import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from pathlib import Path

import asyncio, os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from testcontainers.postgres import PostgresContainer
from backend.databases.data_base.models import usersBase, chatsBase

#.TODO переделать тесты на моки

docker_socket = Path.home() / ".colima/default/docker.sock"
if docker_socket.exists():
    os.environ["DOCKER_HOST"] = f"unix://{docker_socket}"

else:
    docker_socket = Path("/var/run/docker.sock")
    if docker_socket.exists():
        os.environ["DOCKER_HOST"] = f"unix://{docker_socket}"

os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"
os.environ["TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE"] = str(docker_socket)

@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        conn_url = postgres.get_connection_url().replace("postgresql+psycopg2://", "postgresql+asyncpg://")

        yield conn_url


@pytest_asyncio.fixture(scope="session")
async def db_engine(postgres_container):
    engine = create_async_engine(postgres_container, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(usersBase.metadata.create_all)
        await conn.run_sync(chatsBase.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(usersBase.metadata.drop_all)
        await conn.run_sync(chatsBase.metadata.drop_all)


@pytest_asyncio.fixture
async def session(db_engine):
    async with db_engine.connect() as connection:
        trans = await connection.begin()

        Session = async_sessionmaker(
            bind=connection, 
            expire_on_commit=False,
            join_transaction_mode="create_savepoint"
        )
        
        async with Session() as session:
            yield session

        await trans.rollback()