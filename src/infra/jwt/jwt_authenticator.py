import jwt
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException
from jwt import InvalidTokenError
from starlette import status


from src.infra.env import EnvSettings
from src.infra.exception import InfraException
from src.infra.jwt.jwt_dto import CreateJwtTokenDto, JwtToken, JwtPayload


class JwtAuthenticator:
    def __init__(self, env: EnvSettings):
        self.env = env

    @staticmethod
    def create_partial_token(
            data: dict,
            secret_key: str,
            algorithm: str,
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        if to_encode['timedelta']:
            expire = datetime.now(timezone.utc) + to_encode['timedelta']
            del to_encode['timedelta']
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    def _get_default_create_token_params(self, payload: CreateJwtTokenDto, default_timedelta: timedelta) -> dict:
        data = payload.model_dump()
        if data['timedelta'] is None:
            data['timedelta'] = default_timedelta
        return {
            "data": data,
            "secret_key": self.env.TOKEN_SECRET_KEY,
            "algorithm": self.env.TOKEN_ALGORITHM
        }

    def create_access_token(self,
                            access_payload: CreateJwtTokenDto,
                            ) -> str:
        access_token_expires = timedelta(minutes=self.env.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_params = self._get_default_create_token_params(payload=access_payload,
                                                                    default_timedelta=access_token_expires)

        access_token = JwtAuthenticator.create_partial_token(**access_token_params)
        return access_token

    def create_refresh_token(self,
                             refresh_payload: CreateJwtTokenDto,
                             ) -> str:
        refresh_token_expires = timedelta(minutes=self.env.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token_params = self._get_default_create_token_params(payload=refresh_payload,
                                                                     default_timedelta=refresh_token_expires)
        refresh_token = JwtAuthenticator.create_partial_token(**refresh_token_params)
        return refresh_token

    def create_token(self,
                     access_payload: CreateJwtTokenDto,
                     refresh_payload: CreateJwtTokenDto
                     ) -> JwtToken:
        return JwtToken(
            access_token=self.create_access_token(access_payload=access_payload),
            refresh_token=self.create_refresh_token(refresh_payload=refresh_payload)
        )

    def validate_token(self, token: str) -> JwtPayload:
        try:
            payload = jwt.decode(token, self.env.TOKEN_SECRET_KEY, algorithms=[self.env.TOKEN_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="token validation failed",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            return JwtPayload(
                sub=payload.get('sub'),
                exp=payload.get('exp')
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token validation failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception:
            raise InfraException(message="Invalid Token", http_status_code=500)

    def refresh_access_token(self, refresh_token: str) -> JwtToken:
        try:
            payload = jwt.decode(refresh_token, self.env.TOKEN_SECRET_KEY, algorithms=[self.env.TOKEN_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise InfraException(message="Invalid Token", http_status_code=401)
            payload = CreateJwtTokenDto(sub=username)
            return JwtToken(
                refresh_token=refresh_token,
                access_token=self.create_access_token(access_payload=payload)
            )
        except InvalidTokenError:
            raise InfraException(message="Invalid Token", http_status_code=401)
        except Exception:
            raise InfraException(message="Invalid Token", http_status_code=500)
