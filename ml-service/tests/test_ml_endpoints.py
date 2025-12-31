"""
Tests for ML service endpoints.
"""
import pytest
from httpx import AsyncClient


@pytest.fixture
def forecast_request():
    """Sample forecast request."""
    return {
        "product_id": "test-product-123",
        "historical_data": [
            {"date": "2024-01-01", "quantity": 100},
            {"date": "2024-01-02", "quantity": 120},
            {"date": "2024-01-03", "quantity": 95},
            {"date": "2024-01-04", "quantity": 110},
            {"date": "2024-01-05", "quantity": 130},
            {"date": "2024-01-06", "quantity": 105},
            {"date": "2024-01-07", "quantity": 115},
        ],
        "days_ahead": 7,
    }


@pytest.fixture
def anomaly_request():
    """Sample anomaly detection request."""
    return {
        "metrics": [
            {"timestamp": "2024-01-01T00:00:00", "value": 100},
            {"timestamp": "2024-01-01T01:00:00", "value": 102},
            {"timestamp": "2024-01-01T02:00:00", "value": 98},
            {"timestamp": "2024-01-01T03:00:00", "value": 250},  # Anomaly
            {"timestamp": "2024-01-01T04:00:00", "value": 101},
            {"timestamp": "2024-01-01T05:00:00", "value": 99},
        ],
        "sensitivity": 0.95,
    }


@pytest.fixture
def route_optimization_request():
    """Sample route optimization request."""
    return {
        "origin": {"lat": 23.8103, "lng": 90.4125, "name": "Dhaka"},
        "destinations": [
            {"lat": 22.3569, "lng": 91.7832, "name": "Chittagong"},
            {"lat": 24.3636, "lng": 88.6241, "name": "Rajshahi"},
            {"lat": 22.8456, "lng": 89.5403, "name": "Khulna"},
        ],
        "vehicle_capacity": 1000,
    }


class TestMLServiceHealth:
    """Tests for ML service health endpoints."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, ml_client: AsyncClient):
        """Test ML service health check."""
        response = await ml_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestDemandForecasting:
    """Tests for demand forecasting endpoints."""
    
    @pytest.mark.asyncio
    async def test_forecast_success(self, ml_client: AsyncClient, forecast_request: dict):
        """Test successful demand forecast."""
        response = await ml_client.post("/api/v1/predict/demand", json=forecast_request)
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == forecast_request["days_ahead"]
    
    @pytest.mark.asyncio
    async def test_forecast_insufficient_data(self, ml_client: AsyncClient):
        """Test forecast with insufficient historical data."""
        request = {
            "product_id": "test",
            "historical_data": [
                {"date": "2024-01-01", "quantity": 100},
            ],
            "days_ahead": 7,
        }
        response = await ml_client.post("/api/v1/predict/demand", json=request)
        assert response.status_code in [400, 422]


class TestAnomalyDetection:
    """Tests for anomaly detection endpoints."""
    
    @pytest.mark.asyncio
    async def test_anomaly_detection_success(self, ml_client: AsyncClient, anomaly_request: dict):
        """Test successful anomaly detection."""
        response = await ml_client.post("/api/v1/detect/anomalies", json=anomaly_request)
        assert response.status_code == 200
        data = response.json()
        assert "anomalies" in data
        assert "is_anomaly" in data["anomalies"][0]
    
    @pytest.mark.asyncio
    async def test_anomaly_with_threshold(self, ml_client: AsyncClient, anomaly_request: dict):
        """Test anomaly detection with custom threshold."""
        anomaly_request["sensitivity"] = 0.99
        response = await ml_client.post("/api/v1/detect/anomalies", json=anomaly_request)
        assert response.status_code == 200


class TestRouteOptimization:
    """Tests for route optimization endpoints."""
    
    @pytest.mark.asyncio
    async def test_route_optimization_success(
        self, ml_client: AsyncClient, route_optimization_request: dict
    ):
        """Test successful route optimization."""
        response = await ml_client.post(
            "/api/v1/optimize/route", json=route_optimization_request
        )
        assert response.status_code == 200
        data = response.json()
        assert "optimized_route" in data
        assert "total_distance" in data
    
    @pytest.mark.asyncio
    async def test_route_optimization_single_destination(self, ml_client: AsyncClient):
        """Test route optimization with single destination."""
        request = {
            "origin": {"lat": 23.8103, "lng": 90.4125, "name": "Dhaka"},
            "destinations": [
                {"lat": 22.3569, "lng": 91.7832, "name": "Chittagong"},
            ],
            "vehicle_capacity": 1000,
        }
        response = await ml_client.post("/api/v1/optimize/route", json=request)
        assert response.status_code == 200


class TestModelStatus:
    """Tests for model status endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_model_status(self, ml_client: AsyncClient):
        """Test getting model status."""
        response = await ml_client.get("/api/v1/models/status")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
    
    @pytest.mark.asyncio
    async def test_get_model_metrics(self, ml_client: AsyncClient):
        """Test getting model metrics."""
        response = await ml_client.get("/api/v1/models/metrics")
        assert response.status_code == 200


@pytest.fixture
async def ml_client() -> AsyncClient:
    """Create ML service test client."""
    # Note: In actual tests, this would connect to the ML service
    # For unit tests, you might mock the ML service
    from ml_service.app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
