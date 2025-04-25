from pydantic import BaseModel
from datetime import timedelta
from typing import Optional


class CreateJwtTokenDto(BaseModel):
    sub: str  ## username
    aud: str
    timedelta: Optional[timedelta] = None  # type: ignore


class JwtPayload(BaseModel):
    sub: str  ## username
    exp: int
    aud: str


class UserInfoDto(BaseModel):
    username: str
    password: str


class JwtToken(BaseModel):
    access_token: str
    refresh_token: str
