import pytest

from src.async_sqlalchemy_uow import AsyncSqlAlchemyUow
from src.infra.env import EnvSettings
from src.infra.persistence.sqlalchemy.db_session import drop_tables, create_tables, create_persistence
from src.usecase.user_auth_sync_usecase import UserAuthSyncUseCase
from src.usecase.user_auth_usecase import UserAuthUseCase


@pytest.fixture(scope="session")
async def test_env() -> EnvSettings:
    env = EnvSettings.load_test_env()
    drop_tables(env)
    create_tables(env)
    return env


@pytest.fixture(scope="function")
async def uow(test_env) -> AsyncSqlAlchemyUow:
    async_engine, session_maker = create_persistence(test_env)
    return AsyncSqlAlchemyUow(
        session_factory=session_maker,
    )


@pytest.fixture(scope="function")
async def user_auth_usecase(
        test_env: EnvSettings,
        uow: AsyncSqlAlchemyUow,

) -> UserAuthUseCase:
    return UserAuthUseCase(
        env=test_env,
        uow=uow,
    )


@pytest.fixture(scope="function")
async def user_auth_sync_usecase(
        test_env: EnvSettings,
        uow: AsyncSqlAlchemyUow,
) -> UserAuthSyncUseCase:
    return UserAuthSyncUseCase(
        env=test_env,
        uow=uow,
    )
