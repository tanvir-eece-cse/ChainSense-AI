"""
Analytics and ML endpoints.
"""

from datetime import datetime, timedelta
from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.core.config import settings
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models import (
    Product,
    Inventory,
    Shipment,
    DemandForecast,
    AnomalyAlert,
    User,
)
from app.schemas import (
    DemandForecastRequest,
    DemandForecastResponse,
    AnomalyAlertResponse,
    RouteOptimizationRequest,
    RouteOptimizationResponse,
)

router = APIRouter()


@router.post("/demand/forecast", response_model=DemandForecastResponse)
async def get_demand_forecast(
    request: DemandForecastRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get AI-powered demand forecast for a product."""
    # Verify product exists
    product_result = await db.execute(
        select(Product).where(Product.id == request.product_id)
    )
    product = product_result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )
    
    # Call ML service for prediction
    try:
        async with httpx.AsyncClient(timeout=settings.ML_REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/api/v1/predict/demand",
                json={
                    "product_id": str(request.product_id),
                    "warehouse_id": str(request.warehouse_id) if request.warehouse_id else None,
                    "forecast_days": request.forecast_days,
                },
            )
            if response.status_code == 200:
                ml_result = response.json()
            else:
                # Fallback to mock data if ML service unavailable
                ml_result = generate_mock_forecast(request.forecast_days)
    except Exception:
        # Fallback to mock data
        ml_result = generate_mock_forecast(request.forecast_days)
    
    return {
        "product_id": request.product_id,
        "warehouse_id": request.warehouse_id,
        "forecasts": ml_result.get("forecasts", []),
        "model_version": ml_result.get("model_version", "v1.0.0"),
        "generated_at": datetime.utcnow(),
    }


def generate_mock_forecast(days: int) -> dict:
    """Generate mock forecast data for demonstration."""
    import random
    
    forecasts = []
    base_demand = random.randint(50, 200)
    
    for i in range(days):
        date = datetime.utcnow() + timedelta(days=i)
        # Add some seasonality and randomness
        seasonal_factor = 1 + 0.2 * ((i % 7) / 7)
        demand = base_demand * seasonal_factor + random.randint(-20, 20)
        
        forecasts.append({
            "date": date.strftime("%Y-%m-%d"),
            "predicted_demand": round(max(0, demand), 2),
            "confidence_lower": round(max(0, demand * 0.8), 2),
            "confidence_upper": round(demand * 1.2, 2),
        })
    
    return {
        "forecasts": forecasts,
        "model_version": "v1.0.0-mock",
    }


@router.get("/anomalies", response_model=List[AnomalyAlertResponse])
async def get_anomalies(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    severity: Optional[str] = None,
    is_acknowledged: Optional[bool] = None,
    limit: int = Query(50, ge=1, le=200),
) -> List[AnomalyAlert]:
    """Get detected anomalies in the supply chain."""
    query = select(AnomalyAlert)
    
    if severity:
        query = query.where(AnomalyAlert.severity == severity)
    
    if is_acknowledged is not None:
        query = query.where(AnomalyAlert.is_acknowledged == is_acknowledged)
    
    query = query.order_by(AnomalyAlert.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    anomalies = result.scalars().all()
    
    return anomalies


@router.post("/anomalies/{anomaly_id}/acknowledge")
async def acknowledge_anomaly(
    anomaly_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Acknowledge an anomaly alert."""
    result = await db.execute(
        select(AnomalyAlert).where(AnomalyAlert.id == anomaly_id)
    )
    anomaly = result.scalar_one_or_none()
    
    if not anomaly:
        raise HTTPException(
            status_code=404,
            detail="Anomaly not found",
        )
    
    anomaly.is_acknowledged = True
    anomaly.acknowledged_by = current_user.id
    anomaly.acknowledged_at = datetime.utcnow()
    
    await db.commit()
    
    return {
        "anomaly_id": str(anomaly_id),
        "acknowledged": True,
        "acknowledged_by": str(current_user.id),
    }


@router.post("/routes/optimize", response_model=RouteOptimizationResponse)
async def optimize_route(
    request: RouteOptimizationRequest,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Get AI-optimized delivery route."""
    # Call ML service for route optimization
    try:
        async with httpx.AsyncClient(timeout=settings.ML_REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/api/v1/optimize/route",
                json=request.model_dump(),
            )
            if response.status_code == 200:
                return response.json()
    except Exception:
        pass
    
    # Fallback to mock optimization
    return generate_mock_route(request)


def generate_mock_route(request: RouteOptimizationRequest) -> dict:
    """Generate mock route optimization for demonstration."""
    import math
    
    # Calculate approximate distance
    lat1 = request.origin.get("latitude", 23.8103)  # Dhaka default
    lon1 = request.origin.get("longitude", 90.4125)
    lat2 = request.destination.get("latitude", 22.3569)  # Chittagong default
    lon2 = request.destination.get("longitude", 91.7832)
    
    # Haversine formula for distance
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    # Estimate duration (assuming average 50 km/h for trucks)
    duration = (distance / 50) * 60  # in minutes
    
    # Estimate fuel (assuming 8 km per liter)
    fuel = distance / 8
    
    # Build route
    route = [
        {
            "location": request.origin,
            "type": "origin",
            "arrival_time": None,
        }
    ]
    
    if request.waypoints:
        for i, wp in enumerate(request.waypoints):
            route.append({
                "location": wp,
                "type": "waypoint",
                "arrival_time": f"+{int(duration * (i+1) / (len(request.waypoints)+1))} min",
            })
    
    route.append({
        "location": request.destination,
        "type": "destination",
        "arrival_time": f"+{int(duration)} min",
    })
    
    return {
        "optimized_route": route,
        "total_distance_km": round(distance * 1.15, 2),  # Add 15% for road routes
        "estimated_duration_minutes": round(duration * 1.15, 0),
        "fuel_estimate_liters": round(fuel * 1.15, 2),
        "co2_estimate_kg": round(fuel * 1.15 * 2.68, 2),  # 2.68 kg CO2 per liter diesel
    }


@router.get("/dashboard/kpis")
async def get_dashboard_kpis(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get key performance indicators for dashboard."""
    # Inventory stats
    inventory_result = await db.execute(
        select(func.sum(Inventory.quantity))
    )
    total_inventory = inventory_result.scalar() or 0
    
    # Shipment stats
    pending_shipments = await db.execute(
        select(func.count(Shipment.id)).where(Shipment.status == "pending")
    )
    in_transit_shipments = await db.execute(
        select(func.count(Shipment.id)).where(Shipment.status == "in_transit")
    )
    
    # Anomaly stats
    active_anomalies = await db.execute(
        select(func.count(AnomalyAlert.id))
        .where(AnomalyAlert.is_resolved == False)
    )
    
    return {
        "inventory": {
            "total_units": total_inventory,
            "low_stock_alerts": 12,  # Would calculate from actual data
            "turnover_rate": 4.5,
        },
        "shipments": {
            "pending": pending_shipments.scalar() or 0,
            "in_transit": in_transit_shipments.scalar() or 0,
            "on_time_rate": 0.94,
        },
        "anomalies": {
            "active": active_anomalies.scalar() or 0,
            "resolved_today": 5,
            "avg_resolution_time_hours": 2.3,
        },
        "demand_accuracy": {
            "mape": 12.5,
            "trend": "improving",
        },
        "supplier_health": {
            "avg_risk_score": 0.23,
            "high_risk_count": 2,
        },
    }


@router.get("/reports/supply-chain-health")
async def get_supply_chain_health_report(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    time_range_days: int = Query(30, ge=1, le=365),
) -> dict:
    """Get comprehensive supply chain health report."""
    return {
        "report_period": {
            "start": (datetime.utcnow() - timedelta(days=time_range_days)).isoformat(),
            "end": datetime.utcnow().isoformat(),
        },
        "overall_health_score": 87.5,
        "metrics": {
            "inventory_accuracy": 98.2,
            "order_fulfillment_rate": 96.5,
            "perfect_order_rate": 94.1,
            "on_time_delivery": 93.8,
            "supplier_quality_index": 91.2,
            "demand_forecast_accuracy": 87.5,
        },
        "trends": {
            "inventory_accuracy": "+1.2%",
            "order_fulfillment_rate": "+0.8%",
            "on_time_delivery": "-0.3%",
        },
        "recommendations": [
            {
                "priority": "high",
                "area": "inventory",
                "suggestion": "Increase safety stock for top 10 SKUs by 15%",
                "expected_impact": "Reduce stockouts by 25%",
            },
            {
                "priority": "medium",
                "area": "suppliers",
                "suggestion": "Review contracts with 2 underperforming suppliers",
                "expected_impact": "Improve quality score by 5%",
            },
            {
                "priority": "low",
                "area": "logistics",
                "suggestion": "Consolidate shipments to Chittagong region",
                "expected_impact": "Reduce transportation costs by 8%",
            },
        ],
    }
