from pydantic import BaseModel


class SyncUserReq(BaseModel):
    username: str
    password: str
    service_name: str
