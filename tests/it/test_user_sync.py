import pytest

from src.usecase.user_auth_sync_usecase import UserAuthSyncUseCase
from src.usecase.user_auth_usecase import UserAuthUseCase


@pytest.mark.asyncio
async def test_user_sync(
        user_auth_sync_usecase: UserAuthSyncUseCase,
        user_auth_usecase: UserAuthUseCase
):
    username = 'testMan'
    password = '<PASSWORD>'
    service_name = 'test'
    created_user = await user_auth_sync_usecase.sync_user(
        username=username,
        password=password,
        service_name=service_name
    )

    assert created_user is not None
    assert created_user.username == username
