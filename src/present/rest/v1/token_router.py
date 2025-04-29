from fastapi import APIRouter, Depends

from src.dependencies import get_user_auth_usecase
from src.infra.jwt.jwt_dto import JwtToken
from src.infra.presentation.rest_res import RestResponse
from src.present.rest.v1.dto.token import LoginReq
from src.usecase.user_auth_usecase import UserAuthUseCase

rt = APIRouter(tags=["token_router"])


@rt.post("/login")
async def login(
        req: LoginReq,
        user_auth_usecase: UserAuthUseCase = Depends(get_user_auth_usecase),
) -> RestResponse[JwtToken]:
    ret = await user_auth_usecase.create_token(
        username=req.username,
        password=req.password,
        service_name=req.service_name,
    )
    return RestResponse.success(data=ret)
