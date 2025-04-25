from jose import jwt
from typing import Optional


from src.domain.model.user_auth_entity import UserAuthEntity
from src.infra.jwt.jwt_authenticator import JwtAuthenticator
from src.infra.jwt.jwt_dto import CreateJwtTokenDto, JwtPayload, JwtToken
from src.infra.jwt.jwt_validator import JwtValidator


class JwtTokenService:
    def __init__(self, jwt: JwtAuthenticator, jwt_validator: JwtValidator):
        self.jwt_auth = jwt
        self.jwt_validator = jwt_validator

    def get_unverified_claims(self,token: str)->Optional[dict]:
        payload = jwt.get_unverified_claims(token)
        return payload

    def decode_token(self, jwt_token: str, aud: str) -> Optional[JwtPayload]:
        payload = self.jwt_validator.decode_token(token=jwt_token, aud=aud)
        return payload

    def setup_refresh_token(self, user: UserAuthEntity, create_token_dto: CreateJwtTokenDto) -> UserAuthEntity:
        payload = self.jwt_validator.decode_token(token=user.refresh_token, aud=create_token_dto.aud)
        if payload is None:
            refresh_token = self.jwt_auth.create_refresh_token(
                refresh_payload=create_token_dto
            )
            user.setup_refresh_token(refresh_token=refresh_token)
        return user

    def create_jwt_token(self, user: UserAuthEntity, service_name: str) -> JwtToken:
        create_token_dto = CreateJwtTokenDto(
            sub=user.username,
            aud=service_name
        )
        access_token = self.jwt_auth.create_access_token(
            access_payload=create_token_dto
        )
        self.setup_refresh_token(user=user, create_token_dto=create_token_dto)

        return JwtToken(
            access_token=access_token,
            refresh_token=user.refresh_token
        )
