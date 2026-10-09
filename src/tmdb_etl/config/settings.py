from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    tmdb_api_key: str
    tmdb_base_url: str = "https://api.themoviedb.org/3"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
