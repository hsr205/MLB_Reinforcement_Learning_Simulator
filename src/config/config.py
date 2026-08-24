from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url: str = Field(..., description="Initial URL to start web scrapping from")


settings = Settings()
