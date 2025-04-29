from src.async_sqlalchemy_uow import AsyncSqlAlchemyUow
from src.infra.env import EnvSettings
from src.infra.persistence.sqlalchemy.db_session import create_persistence
from src.usecase.user_auth_sync_usecase import UserAuthSyncUseCase
from src.usecase.user_auth_usecase import UserAuthUseCase

env = EnvSettings()
engine, session_maker = create_persistence(env)
uow = AsyncSqlAlchemyUow(session_factory=session_maker)
user_auth_sync_usecase = UserAuthSyncUseCase(env=env, uow=uow)
user_auth_usecase = UserAuthUseCase(env=env, uow=uow)


async def get_env() -> EnvSettings:
    return env


async def get_user_auth_sync_usecase() -> UserAuthSyncUseCase:
    return user_auth_sync_usecase


async def get_user_auth_usecase() -> UserAuthUseCase:
    return user_auth_usecase
