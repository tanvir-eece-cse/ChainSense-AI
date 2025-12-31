"""
Configuration for ML Service.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "ChainSense-AI ML Service"
    PROJECT_DESCRIPTION: str = "Machine Learning Service for Supply Chain Intelligence"
    VERSION: str = "1.0.0"

    # Model paths
    MODEL_DIR: str = "./models"
    DEMAND_MODEL_PATH: str = "./models/demand_forecast.pkl"
    ANOMALY_MODEL_PATH: str = "./models/anomaly_detector.pkl"
    ROUTE_MODEL_PATH: str = "./models/route_optimizer.pkl"

    # MLflow
    MLFLOW_TRACKING_URI: str = "sqlite:///mlflow.db"

    # Inference settings
    MAX_FORECAST_DAYS: int = 365
    ANOMALY_THRESHOLD: float = 0.5
    
    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
