from src.async_sqlalchemy_uow import AsyncSqlAlchemyUow
from src.infra.env import EnvSettings
from src.infra.exception import UseCaseException
from src.infra.hash import BCrypt
from src.infra.jwt.jwt_authenticator import JwtAuthenticator
from src.infra.jwt.jwt_dto import CreateJwtTokenDto


class UserAuthUseCase:
    def __init__(self,
                 env: EnvSettings,
                 uow: AsyncSqlAlchemyUow,
                 ):
        self.env = env
        self.bcrpy = BCrypt()
        self.jwt = JwtAuthenticator(env=env)
        self.uow = uow

    async def create_token(self,
                           username: str,
                           service_name: str,
                           password: str):
        async with self.uow:
            user = await self.uow.user_auth_repository.get_user_by_username(
                username=username
            )
            exception = UseCaseException("invalid user", http_status_code=401)
            if not user:
                raise exception
            is_password = self.bcrpy.verify_password(plain_password=password, hashed_password=user.password)
            if not is_password:
                raise exception

            check_service = user.check_service(service_name=service_name)
            if not check_service:
                raise exception

            user.deactivate_all_tokens()
            create_token_dto = CreateJwtTokenDto(
                sub=username
            )
            jwt_dto = self.jwt.create_token(
                access_payload=create_token_dto,
                refresh_payload=create_token_dto
            )
            user.create_token(
                access_token=jwt_dto.access_token,
                refresh_token=jwt_dto.refresh_token,
            )
            self.uow.add(user)
            await self.uow.commit()
            return jwt_dto
