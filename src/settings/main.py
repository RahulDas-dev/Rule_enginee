from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from .appsettings import AppSettings
from .dbsettings import DbSettings

Environments = Literal["dev", "prod", "test", "demo"]
LogLevel = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR"]


class Settings(BaseSettings):
    """Application settings.

    These parameters can be configured
    with environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".settings",
        env_prefix="RE_",
        frozen=True,
        str_strip_whitespace=True,
        env_nested_delimiter="__",
    )

    environment: Environments = "dev"
    app: AppSettings
    db: DbSettings

    @property
    def is_production(self) -> bool:
        return self.environment == "prod"

    @property
    def is_development(self) -> bool:
        return self.environment == "dev"
