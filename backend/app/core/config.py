"""
Core configuration module for ChainSense-AI Backend.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Project Info
    PROJECT_NAME: str = "ChainSense-AI"
    PROJECT_DESCRIPTION: str = "AI-Powered Supply Chain Intelligence & Security Platform"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    SHOW_DOCS: bool = True

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/chainsense"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 300

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://chainsense-ai.com",
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # ML Service
    ML_SERVICE_URL: str = "http://localhost:8001"
    ML_REQUEST_TIMEOUT: int = 30

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # External Services
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
