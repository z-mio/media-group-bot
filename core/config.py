from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: str
    api_id: str
    api_hash: str
    bot_proxy: str | None = Field(default=None)
    bot_workdir: Path = Field(default=Path("sessions"))
    debug: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        """模型初始化后的操作"""
        self.bot_workdir.mkdir(parents=True, exist_ok=True)

    @field_validator("bot_proxy", mode="before")
    @classmethod
    def proxy_config(cls, v: str | None = None) -> str | None:
        url = urlparse(v) if v else None
        if not url:
            return None
        if url.hostname is None or url.port is None:
            raise ValueError(f"Invalid proxy url: {v}")
        return v

    @property
    def bot_session_name(self) -> str:
        return f"bot_{self.bot_token.split(':')[0]}"


bs = BotSettings()  # type: ignore
