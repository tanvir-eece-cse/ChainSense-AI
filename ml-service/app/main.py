"""
ChainSense-AI ML Service
Machine Learning inference service for supply chain intelligence.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.api.v1 import api_router
from app.core.config import settings
from app.models.model_manager import ModelManager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan manager."""
    # Startup - Load ML models
    app.state.model_manager = ModelManager()
    await app.state.model_manager.load_models()
    yield
    # Shutdown
    pass


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    # Prometheus metrics
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    return app


app = create_application()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ChainSense-AI ML Service",
        "version": settings.VERSION,
        "endpoints": {
            "predict_demand": "/api/v1/predict/demand",
            "detect_anomaly": "/api/v1/detect/anomaly",
            "optimize_route": "/api/v1/optimize/route",
            "models_status": "/api/v1/models/status",
        },
    }
