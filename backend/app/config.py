from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://transit:transit@db:5432/transit_db"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # TDX API (https://tdx.transportdata.tw)
    tdx_client_id: str = ""
    tdx_client_secret: str = ""
    tdx_base_url: str = "https://tdx.transportdata.tw/api/basic"
    tdx_auth_url: str = (
        "https://tdx.transportdata.tw/auth/realms/TDXConnect"
        "/protocol/openid-connect/token"
    )

    # App
    app_env: str = "development"
    debug: bool = True
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]


settings = Settings()
