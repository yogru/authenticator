from typing import Optional

from pydantic import BaseModel

from src.domain.model.user_auth_entity import UserAuthEntity
from src.infra.jwt.jwt_authenticator import JwtAuthenticator
from src.infra.jwt.jwt_dto import CreateJwtTokenDto
from src.infra.jwt.jwt_validator import JwtValidator


class JwtTokenDto(BaseModel):
    access_token: str
    refresh_token: str


class JwtTokenService:
    def __init__(self, jwt: JwtAuthenticator, jwt_validator: JwtValidator):
        self.jwt = jwt
        self.jwt_validator = jwt_validator

    def decode_token(self, jwt_token: str) -> Optional[JwtTokenDto]:
        payload = self.jwt_validator.decode_token(token=jwt_token)
        return payload

    def setup_refresh_token(self, user: UserAuthEntity) -> UserAuthEntity:
        payload = self.jwt_validator.decode_token(token=user.refresh_token)
        if payload is None:
            create_token_dto = CreateJwtTokenDto(
                sub=user.username
            )
            refresh_token = self.jwt.create_refresh_token(
                refresh_payload=create_token_dto
            )
            user.setup_refresh_token(refresh_token=refresh_token)
        return user

    def create_jwt_token(self, user: UserAuthEntity) -> JwtTokenDto:
        create_token_dto = CreateJwtTokenDto(
            sub=user.username
        )
        access_token = self.jwt.create_access_token(
            access_payload=create_token_dto
        )
        self.setup_refresh_token(user=user)

        return JwtTokenDto(
            access_token=access_token,
            refresh_token=user.refresh_token
        )
