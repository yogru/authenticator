import pytest

from src.async_sqlalchemy_uow import AsyncSqlAlchemyUow
from src.infra.env import EnvSettings
from src.infra.persistence.sqlalchemy.db_session import drop_tables, create_tables, create_persistence
from src.usecase.user_auth_sync_usecase import UserAuthSyncUseCase
from src.usecase.user_auth_usecase import UserAuthUseCase


@pytest.fixture(scope="session")
def test_env() -> EnvSettings:
    env = EnvSettings.load_test_env()
    return env


@pytest.fixture(scope="session")
def persistence(test_env: EnvSettings):
    """
        여기서 디비 한 번 날리고 시작함.
    """
    drop_tables(test_env)
    create_tables(test_env)
    return create_persistence(test_env)  # 비동기 엔진 생성


@pytest.fixture(scope="function")
def uow(persistence) -> AsyncSqlAlchemyUow:
    async_engine, session_maker = persistence
    return AsyncSqlAlchemyUow(
        session_factory=session_maker,
    )


@pytest.fixture(scope="function")
def user_auth_usecase(
        test_env: EnvSettings,
        uow: AsyncSqlAlchemyUow,

) -> UserAuthUseCase:
    return UserAuthUseCase(
        env=test_env,
        uow=uow,
    )


@pytest.fixture(scope="function")
def user_auth_sync_usecase(
        test_env: EnvSettings,
        uow: AsyncSqlAlchemyUow,
) -> UserAuthSyncUseCase:
    return UserAuthSyncUseCase(
        env=test_env,
        uow=uow,
    )
