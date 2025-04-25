from src.infra.env import EnvSettings
from src.infra.exception import InfraException


class InternalSecretValidator:
    def __init__(self, env:EnvSettings):
        self.env = env


    def validate_secret(self,secret_code:str):
        if secret_code != self.env.X_INTERNAL_SECRET:
            raise InfraException(message='Invalid internal secret',http_status_code=403)