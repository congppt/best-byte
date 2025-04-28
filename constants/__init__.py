import os


DB_URL = (
    os.getenv("DB_URL")
    or "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
)
CACHE_URL = os.getenv("CACHE_URL") or "redis://localhost:6379"
ENV = os.getenv("ENV") or "local"
IS_PRODUCTION = ENV == "production"
