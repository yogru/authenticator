from src.async_sqlalchemy_uow import AsyncSqlAlchemyUow
from src.domain.model.user_auth_entity import UserAuthEntity
from src.infra.env import EnvSettings
from src.usecase.dto.user_auth_dto import SimpleUserAuthDto


class UserAuthSyncUseCase:
    def __init__(self,
                 env: EnvSettings,
                 uow: AsyncSqlAlchemyUow,
                 ):
        self.env = env
        self.uow = uow

    async def sync_user(self,
                        username: str,
                        password: str,
                        service_name: str
                        ) -> SimpleUserAuthDto:
        async with self.uow:
            found_user = await self.uow.user_auth_repository.get_user_by_username(
                username=username,
            )
            if found_user is None:
                found_user = UserAuthEntity(
                    username=username,
                    password=password,
                )
            found_user.sync_service(service_name=service_name)
            self.uow.add(found_user)
            await self.uow.commit()
            return SimpleUserAuthDto.of(found_user)
