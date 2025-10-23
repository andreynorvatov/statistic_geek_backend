from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        extra="ignore",
    )
    VERSION: str
    PROJECT_NAME: str

    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "production"] = "local"


_ROOT_DIRECTORY: Path = Path(__file__).resolve().parent.parent.parent
env_file_abs_path = Path.joinpath(_ROOT_DIRECTORY, ".env")

settings = Settings(_env_file=env_file_abs_path)  # type: ignore
