from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017/ims_signals"
    postgres_dsn: str = "postgresql+asyncpg://ims_user:ims_pass@localhost:5432/ims_db"
    redis_url: str = "redis://localhost:6379/0"
    rate_limit_per_second: int = 500
    debounce_window_seconds: int = 10
    debounce_threshold: int = 100
    queue_max_size: int = 50000

    class Config:
        env_file = ".env"


settings = Settings()