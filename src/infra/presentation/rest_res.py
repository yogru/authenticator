from typing import Optional, TypeVar, Generic
from datetime import datetime

from pydantic import BaseModel, field_serializer

T = TypeVar('T')


class RestResponse(BaseModel, Generic[T]):
    ok: bool
    http_status_code: int
    data: Optional[T]
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    response_at: datetime = None

    @field_serializer('response_at')
    def serialize_dt(self, response_at: datetime, _info):
        return response_at.timestamp()

    @staticmethod
    def success(data: T, http_status_code: int = 200) -> 'RestResponse[T]':
        return RestResponse(
            response_at=datetime.now(),
            ok=True,
            http_status_code=http_status_code,
            data=data,
        )

    @staticmethod
    def failure(error_code: str, error_message: str, http_status_code: int = 400) -> 'RestResponse[T]':
        return RestResponse(
            response_at=datetime.now(),
            ok=False,
            data=None,  # 데이터가 없으므로 None
            http_status_code=http_status_code,
            error_code=error_code,
            error_message=error_message,
        )

    # @staticmethod
    # def of_pageable(page_result: PageResult, http_status_code: int = 200) -> 'RestResponse[PageResult[T]]':
    #     return RestResponse(
    #         response_at=datetime.now(),
    #         ok=True,
    #         http_status_code=http_status_code,
    #         data=page_result,
    #     )
