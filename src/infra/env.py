from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

ModeType = Literal['service', 'test']
EnvironmentType = Literal["prod", 'dev', "local"]


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f".env")

    MODE: ModeType = 'service'
    ENV_TYPE: EnvironmentType = 'local'
    CORN_HOST: str = "0.0.0.0"
    UVICORN_PORT: int = 9200

    ### DATABASE
    DB_USER: str = "postgres"
    DB_PASS: str = 'aio2o0656)^%^'
    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 5432
    DB_NAME: str = "auth"

    ## jwt
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    TOKEN_SECRET_KEY: str
    TOKEN_ALGORITHM: str = "HS256"

    def get_async_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_postgres_url(self) -> str:
        """
        Sync (동기) 버전의 PostgreSQL 접속 URL을 반환
        예: "postgresql://user:pass@host:port/dbname"
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @staticmethod
    def load_env() -> "EnvSettings":
        target_env_file = f".env"

        class ConfiguredEnvSettings(EnvSettings):
            model_config = SettingsConfigDict(env_file=target_env_file)

        ConfiguredEnvSettings.model_rebuild()
        return ConfiguredEnvSettings()

    @staticmethod
    def load_test_env() -> "EnvSettings":
        target_env_file = f".env.test"

        class ConfiguredEnvSettings(EnvSettings):
            model_config = SettingsConfigDict(env_file=target_env_file)

        ConfiguredEnvSettings.model_rebuild()
        return ConfiguredEnvSettings()
