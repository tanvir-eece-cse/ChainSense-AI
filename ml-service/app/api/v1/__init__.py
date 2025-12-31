"""
ML API Router.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import predict, detect, optimize, models

api_router = APIRouter()

api_router.include_router(predict.router, prefix="/predict", tags=["Prediction"])
api_router.include_router(detect.router, prefix="/detect", tags=["Detection"])
api_router.include_router(optimize.router, prefix="/optimize", tags=["Optimization"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
