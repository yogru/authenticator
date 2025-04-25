from src.async_sqlalchemy_uow import AsyncSqlAlchemyUow
from src.domain.service.jwt_token_service import JwtTokenService, JwtTokenDto
from src.infra.env import EnvSettings
from src.infra.exception import UseCaseException
from src.infra.hash import BCrypt
from src.infra.jwt.jwt_authenticator import JwtAuthenticator
from src.infra.jwt.jwt_dto import CreateJwtTokenDto
from src.infra.jwt.jwt_validator import JwtValidator


class UserAuthUseCase:
    def __init__(self,
                 env: EnvSettings,
                 uow: AsyncSqlAlchemyUow,
                 ):
        self.env = env
        self.bcrpy = BCrypt()
        self.jwt_token_service = JwtTokenService(
            jwt=JwtAuthenticator(env=env),
            jwt_validator=JwtValidator(env=env),
        )
        self.uow = uow

    async def create_token(self,
                           username: str,
                           service_name: str,
                           password: str) -> JwtTokenDto:
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

            jwt_dto = self.jwt_token_service.create_jwt_token(
                user=user,
            )
            self.uow.add(user)
            await self.uow.commit()
            return jwt_dto

    async def refresh_token(self, refresh_token: str) -> JwtTokenDto:
        async with self.uow:
            exception = UseCaseException("invalid token", http_status_code=401)
            payload = self.jwt_token_service.decode_token(
                jwt_token=refresh_token
            )
            if payload is None:
                raise exception

            user = await self.uow.user_auth_repository.get_user_by_username(
                username=payload.sub
            )
            if not user:
                raise exception

            user.check_refresh_token(refresh_token=refresh_token)
            jwt_dto = self.jwt_token_service.create_jwt_token(
                user=user,
            )
            self.uow.add(user)
            await self.uow.commit()
            return jwt_dto
