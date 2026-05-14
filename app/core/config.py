from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite:///./goatly.db"

    SECRET_KEY: str = "change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: str = (
        "http://localhost:3000,"
        "http://localhost:8080,"
        "http://localhost:4200,"
        "http://localhost:5555"
    )

    SEED_ON_STARTUP: bool = False

    # Sprint 4: Caching — Supabase Storage credentials for carnet upload
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()