from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    FLASK_ENV: str = "development"
    FLASK_DEBUG: bool = True
    FLASK_RUN_HOST: str = "localhost"
    FLASK_RUN_PORT: int = 5000
    JWT_SECRET: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
