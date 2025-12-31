# ChainSense AI - API Documentation

## Overview

The ChainSense AI API provides comprehensive supply chain management capabilities powered by machine learning. This RESTful API follows OpenAPI 3.0 specification.

## Base URL

- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://api.chainsense.ai/api/v1`

## Authentication

All API endpoints (except `/auth/login` and `/auth/register`) require authentication using JWT Bearer tokens.

### Obtaining a Token

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Using the Token

Include the token in the Authorization header:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get tokens |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Get current user info |

### Suppliers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/suppliers` | List all suppliers |
| POST | `/suppliers` | Create a new supplier |
| GET | `/suppliers/{id}` | Get supplier details |
| PUT | `/suppliers/{id}` | Update a supplier |
| DELETE | `/suppliers/{id}` | Delete a supplier |
| GET | `/suppliers/{id}/risk` | Get supplier risk assessment |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List all products |
| POST | `/products` | Create a new product |
| GET | `/products/{id}` | Get product details |
| PUT | `/products/{id}` | Update a product |
| DELETE | `/products/{id}` | Delete a product |

### Inventory

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | List inventory items |
| POST | `/inventory` | Add inventory |
| GET | `/inventory/{id}` | Get inventory details |
| PUT | `/inventory/{id}` | Update inventory |
| POST | `/inventory/adjust` | Adjust inventory levels |
| GET | `/inventory/low-stock` | Get low stock alerts |

### Shipments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/shipments` | List all shipments |
| POST | `/shipments` | Create a shipment |
| GET | `/shipments/{id}` | Get shipment details |
| PUT | `/shipments/{id}` | Update a shipment |
| GET | `/shipments/{id}/tracking` | Get tracking info |
| POST | `/shipments/{id}/status` | Update shipment status |

### Analytics (ML-Powered)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analytics/forecast` | Get demand forecast |
| POST | `/analytics/anomaly-detect` | Detect anomalies |
| POST | `/analytics/optimize-route` | Optimize delivery routes |
| GET | `/analytics/dashboard` | Get dashboard metrics |
| GET | `/analytics/insights` | Get AI-generated insights |

## Request/Response Examples

### Create Supplier

```http
POST /suppliers
Content-Type: application/json
Authorization: Bearer {token}

{
  "name": "ABC Electronics Ltd",
  "code": "SUP-001",
  "contact_email": "contact@abcelectronics.com",
  "contact_phone": "+880-1711-000000",
  "address": "123 Industrial Area, Dhaka",
  "city": "Dhaka",
  "country": "Bangladesh",
  "category": "Electronics"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-here",
  "name": "ABC Electronics Ltd",
  "code": "SUP-001",
  "contact_email": "contact@abcelectronics.com",
  "contact_phone": "+880-1711-000000",
  "address": "123 Industrial Area, Dhaka",
  "city": "Dhaka",
  "country": "Bangladesh",
  "category": "Electronics",
  "risk_score": 0.0,
  "reliability_score": 0.0,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Demand Forecast

```http
POST /analytics/forecast
Content-Type: application/json
Authorization: Bearer {token}

{
  "product_id": "uuid-here",
  "days_ahead": 30,
  "include_confidence": true
}
```

**Response:**
```json
{
  "product_id": "uuid-here",
  "forecast": [
    {
      "date": "2024-02-01",
      "predicted_demand": 150,
      "confidence_lower": 120,
      "confidence_upper": 180
    }
  ],
  "model_accuracy": 0.94,
  "recommendation": "Consider increasing inventory by 15%"
}
```

### Route Optimization

```http
POST /analytics/optimize-route
Content-Type: application/json
Authorization: Bearer {token}

{
  "origin": {
    "lat": 23.8103,
    "lng": 90.4125,
    "name": "Dhaka Warehouse"
  },
  "destinations": [
    {"lat": 22.3569, "lng": 91.7832, "name": "Chittagong"},
    {"lat": 24.3636, "lng": 88.6241, "name": "Rajshahi"},
    {"lat": 22.8456, "lng": 89.5403, "name": "Khulna"}
  ],
  "vehicle_capacity": 1000
}
```

**Response:**
```json
{
  "optimized_route": [
    {"name": "Dhaka Warehouse", "order": 0},
    {"name": "Rajshahi", "order": 1},
    {"name": "Khulna", "order": 2},
    {"name": "Chittagong", "order": 3}
  ],
  "total_distance_km": 850.5,
  "estimated_time_hours": 14.2,
  "fuel_cost_estimate": 8500,
  "savings_vs_original": {
    "distance_saved_km": 150.3,
    "time_saved_hours": 2.5,
    "cost_saved": 1500
  }
}
```

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message here",
  "status_code": 400,
  "error_code": "VALIDATION_ERROR"
}
```

### Common Error Codes

| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 400 | VALIDATION_ERROR | Invalid request data |
| 401 | UNAUTHORIZED | Authentication required |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Resource already exists |
| 422 | UNPROCESSABLE | Business logic error |
| 429 | RATE_LIMITED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |

## Rate Limiting

- **Anonymous**: 100 requests/minute
- **Authenticated**: 1000 requests/minute
- **ML Endpoints**: 100 requests/minute

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705312800
```

## Pagination

List endpoints support pagination:

```http
GET /suppliers?page=1&per_page=20&sort=created_at&order=desc
```

**Response:**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "pages": 8
}
```

## Filtering

Most list endpoints support filtering:

```http
GET /inventory?status=low_stock&warehouse_id=uuid&min_quantity=10
```

## Webhooks

Configure webhooks for real-time notifications:

```http
POST /webhooks
Content-Type: application/json
Authorization: Bearer {token}

{
  "url": "https://your-server.com/webhook",
  "events": ["shipment.delivered", "inventory.low_stock", "anomaly.detected"],
  "secret": "your-webhook-secret"
}
```

## SDK & Libraries

- **Python**: `pip install chainsense-ai`
- **JavaScript**: `npm install @chainsense/api-client`
- **OpenAPI Spec**: Available at `/api/v1/openapi.json`

## Support

- **Documentation**: https://docs.chainsense.ai
- **GitHub Issues**: https://github.com/tanvir-eece-cse/ChainSense-AI/issues
- **Email**: support@chainsense.ai
