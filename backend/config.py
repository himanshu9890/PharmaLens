from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://pharmalens:pharmalens@localhost:5432/pharmalens"

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 86400  # 24 hours

    # ClinicalTrials.gov
    ctgov_base_url: str = "https://clinicaltrials.gov/api/v2"
    ctgov_page_size: int = 25

    # NLM MeSH API
    mesh_api_url: str = "https://id.nlm.nih.gov/mesh"

    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    # Set CORS_ALLOW_ALL=true on Render to accept any Vercel preview URL,
    # or list specific origins in CORS_ORIGINS.
    cors_allow_all: bool = False
    debug: bool = False


settings = Settings()
