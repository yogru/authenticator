import pytest
import asyncio

from src.usecase.user_auth_sync_usecase import UserAuthSyncUseCase
from src.usecase.user_auth_usecase import UserAuthUseCase


@pytest.mark.asyncio
async def test_create_token_case1(
        user_auth_sync_usecase: UserAuthSyncUseCase,
        user_auth_usecase: UserAuthUseCase
):
    username = 'refreshTest'
    password = '1212PASSWORD>'
    service_name = 'test'
    created_user = await user_auth_sync_usecase.sync_user(
        username=username,
        password=password,
        service_name=service_name
    )
    token1 = await user_auth_usecase.create_token(
        username=username,
        service_name=service_name,
        password=password,
    )

    await asyncio.sleep(1)  # ✅ 1초 대기
    token2 = await user_auth_usecase.refresh_token(
        refresh_token=token1.refresh_token,
    )

    assert token1.access_token != token2.access_token
    assert token1.refresh_token == token2.refresh_token
