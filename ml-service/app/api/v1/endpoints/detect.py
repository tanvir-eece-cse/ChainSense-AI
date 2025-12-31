"""
Anomaly detection endpoints.
"""

from typing import Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter()


class AnomalyDetectionRequest(BaseModel):
    """Request model for anomaly detection."""
    entity_type: str  # product, supplier, shipment, inventory
    entity_id: str
    features: Dict[str, float]


class AnomalyDetectionResponse(BaseModel):
    """Response model for anomaly detection."""
    entity_type: str
    entity_id: str
    is_anomaly: bool
    anomaly_score: float
    features_analyzed: List[str]
    alert: Optional[dict] = None


@router.post("/anomaly", response_model=AnomalyDetectionResponse)
async def detect_anomaly(
    request_data: AnomalyDetectionRequest,
    request: Request,
) -> dict:
    """
    Detect anomalies in supply chain data.
    
    Uses Isolation Forest algorithm for unsupervised anomaly detection.
    """
    model_manager = request.app.state.model_manager
    
    result = model_manager.anomaly_model.detect(
        entity_type=request_data.entity_type,
        entity_id=request_data.entity_id,
        features=request_data.features,
    )
    
    return result


class BatchAnomalyRequest(BaseModel):
    """Request for batch anomaly detection."""
    entities: List[AnomalyDetectionRequest]


@router.post("/anomaly/batch")
async def detect_anomaly_batch(
    request_data: BatchAnomalyRequest,
    request: Request,
) -> dict:
    """Detect anomalies in multiple entities."""
    model_manager = request.app.state.model_manager
    
    results = []
    anomaly_count = 0
    
    for entity in request_data.entities[:100]:  # Limit to 100 entities
        result = model_manager.anomaly_model.detect(
            entity_type=entity.entity_type,
            entity_id=entity.entity_id,
            features=entity.features,
        )
        results.append(result)
        if result["is_anomaly"]:
            anomaly_count += 1
    
    return {
        "results": results,
        "total_processed": len(results),
        "anomalies_found": anomaly_count,
        "anomaly_rate": round(anomaly_count / len(results) if results else 0, 3),
        "processed_at": datetime.utcnow().isoformat(),
    }


@router.post("/anomaly/realtime")
async def realtime_anomaly_stream(
    request_data: AnomalyDetectionRequest,
    request: Request,
) -> dict:
    """
    Real-time anomaly detection for streaming data.
    
    Optimized for low-latency inference.
    """
    model_manager = request.app.state.model_manager
    
    start_time = datetime.utcnow()
    
    result = model_manager.anomaly_model.detect(
        entity_type=request_data.entity_type,
        entity_id=request_data.entity_id,
        features=request_data.features,
    )
    
    end_time = datetime.utcnow()
    latency_ms = (end_time - start_time).total_seconds() * 1000
    
    result["latency_ms"] = round(latency_ms, 2)
    result["timestamp"] = end_time.isoformat()
    
    return result
