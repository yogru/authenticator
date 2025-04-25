from typing import Optional

import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from fastapi import HTTPException
from starlette import status

from src.infra.env import EnvSettings
from src.infra.exception import InfraException
from src.infra.jwt.jwt_dto import JwtPayload


class JwtValidator:
    def __init__(self, env: EnvSettings):
        self.env = env

    def decode_token(self, token: str) -> Optional[JwtPayload]:
        try:
            if not token or token.strip() == "":
                return None
            payload = jwt.decode(token, self.env.TOKEN_SECRET_KEY, algorithms=[self.env.TOKEN_ALGORITHM])
            username: str = payload.get("sub")
            exp = payload.get('exp')

            if username is None or exp is None:
                return None
            return JwtPayload(
                sub=payload.get('sub'),
                exp=payload.get('exp')
            )
        except ExpiredSignatureError:
            # 명확히 만료 처리
            print("Token expired")
            return None
        except InvalidTokenError as e:
            return None


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
    except ExpiredSignatureError:
        # 명확히 만료 처리
        print("Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise InfraException(message="Invalid Token", http_status_code=500)
