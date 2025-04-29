from pydantic import BaseModel


class LoginReq(BaseModel):
    username: str
    password: str
    service_name: str
