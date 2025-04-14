import pytest

from src.usecase.user_auth_sync_usecase import UserAuthSyncUseCase
from src.usecase.user_auth_usecase import UserAuthUseCase


@pytest.mark.asyncio
async def test_create_token(
        user_auth_sync_usecase: UserAuthSyncUseCase,
        user_auth_usecase: UserAuthUseCase
):
    username = 'testMaq12n'
    password = '1212PASSWORD>'
    service_name = 'test'
    created_user = await user_auth_sync_usecase.sync_user(
        username=username,
        password=password,
        service_name=service_name
    )

    token = await user_auth_usecase.create_token(
        username=username,
        service_name=service_name,
        password=password,
    )

    print("토큰 한 번 볼까??> ", token)
    assert token is not None
    assert created_user is not None
    assert username == created_user.username
    assert token.access_token is not None
    assert token.refresh_token is not None
