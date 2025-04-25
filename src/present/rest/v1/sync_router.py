from fastapi import APIRouter, Depends, Request, Header

from src.dependencies import get_env, get_user_auth_sync_usecase
from src.infra.env import EnvSettings
from src.infra.exception import PresentationException
from src.infra.presentation.rest_res import RestResponse
from src.present.rest.v1.dto.sync_user import SyncUserReq
from src.usecase.dto.user_auth_dto import SimpleUserAuthDto
from src.usecase.user_auth_sync_usecase import UserAuthSyncUseCase

rt = APIRouter(tags=["auth_router"])


@rt.post("/sync/user")
async def sync_user(
        req: SyncUserReq,
        x_internal_secret: str = Header(...),
        env: EnvSettings = Depends(get_env),
        user_auth_sync_usecase: UserAuthSyncUseCase = Depends(get_user_auth_sync_usecase),
) -> RestResponse[SimpleUserAuthDto]:
    if env.X_INTERNAL_SECRET != x_internal_secret:
        raise PresentationException(
            message="X-Internal-Secret does not match",
            http_status_code=403,
        )
    ret = await user_auth_sync_usecase.sync_user(
        username=req.username,
        password=req.password,
        service_name=req.service_name,
    )
    return RestResponse.success(data=ret)
