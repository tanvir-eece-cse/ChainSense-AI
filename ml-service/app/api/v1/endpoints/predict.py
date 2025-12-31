"""
Prediction endpoints for demand forecasting.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter()


class DemandPredictionRequest(BaseModel):
    """Request model for demand prediction."""
    product_id: str
    warehouse_id: Optional[str] = None
    forecast_days: int = Field(default=30, ge=1, le=365)
    historical_data: Optional[List[float]] = None


class DemandPredictionResponse(BaseModel):
    """Response model for demand prediction."""
    product_id: str
    warehouse_id: Optional[str] = None
    forecasts: List[dict]
    model_version: str
    generated_at: datetime


@router.post("/demand", response_model=DemandPredictionResponse)
async def predict_demand(
    request_data: DemandPredictionRequest,
    request: Request,
) -> dict:
    """
    Generate demand forecast for a product.
    
    Uses LSTM-based model with seasonal decomposition for accurate predictions.
    """
    model_manager = request.app.state.model_manager
    
    forecasts = model_manager.demand_model.predict(
        product_id=request_data.product_id,
        forecast_days=request_data.forecast_days,
        historical_data=request_data.historical_data,
    )
    
    return {
        "product_id": request_data.product_id,
        "warehouse_id": request_data.warehouse_id,
        "forecasts": forecasts,
        "model_version": "1.0.0",
        "generated_at": datetime.utcnow(),
    }


class BatchDemandRequest(BaseModel):
    """Request for batch demand prediction."""
    product_ids: List[str]
    forecast_days: int = Field(default=30, ge=1, le=365)


@router.post("/demand/batch")
async def predict_demand_batch(
    request_data: BatchDemandRequest,
    request: Request,
) -> dict:
    """Generate demand forecasts for multiple products."""
    model_manager = request.app.state.model_manager
    
    results = {}
    for product_id in request_data.product_ids[:50]:  # Limit to 50 products
        forecasts = model_manager.demand_model.predict(
            product_id=product_id,
            forecast_days=request_data.forecast_days,
        )
        results[product_id] = forecasts
    
    return {
        "predictions": results,
        "products_processed": len(results),
        "model_version": "1.0.0",
        "generated_at": datetime.utcnow().isoformat(),
    }
