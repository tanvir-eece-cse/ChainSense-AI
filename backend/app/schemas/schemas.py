"""
Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Any, Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# ============= User Schemas =============

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating user."""
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: UUID
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============= Auth Schemas =============

class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


# ============= Supplier Schemas =============

class SupplierBase(BaseModel):
    """Base supplier schema."""
    name: str = Field(..., min_length=2, max_length=255)
    code: str = Field(..., min_length=2, max_length=50)
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class SupplierCreate(SupplierBase):
    """Schema for creating supplier."""
    pass


class SupplierUpdate(BaseModel):
    """Schema for updating supplier."""
    name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierResponse(SupplierBase):
    """Schema for supplier response."""
    id: UUID
    risk_score: float
    reliability_score: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Product Schemas =============

class ProductBase(BaseModel):
    """Base product schema."""
    sku: str = Field(..., min_length=3, max_length=100)
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    unit_price: float = Field(..., gt=0)
    unit_cost: Optional[float] = None
    weight: Optional[float] = None
    dimensions: Optional[dict] = None


class ProductCreate(ProductBase):
    """Schema for creating product."""
    supplier_id: Optional[UUID] = None
    min_stock_level: int = 0
    max_stock_level: int = 1000
    reorder_point: int = 100
    lead_time_days: int = 7


class ProductUpdate(BaseModel):
    """Schema for updating product."""
    name: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[float] = None
    unit_cost: Optional[float] = None
    min_stock_level: Optional[int] = None
    reorder_point: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: UUID
    supplier_id: Optional[UUID] = None
    min_stock_level: int
    max_stock_level: int
    reorder_point: int
    lead_time_days: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Warehouse Schemas =============

class WarehouseBase(BaseModel):
    """Base warehouse schema."""
    name: str = Field(..., min_length=2, max_length=255)
    code: str = Field(..., min_length=2, max_length=50)
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = None


class WarehouseCreate(WarehouseBase):
    """Schema for creating warehouse."""
    pass


class WarehouseResponse(WarehouseBase):
    """Schema for warehouse response."""
    id: UUID
    current_utilization: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Inventory Schemas =============

class InventoryBase(BaseModel):
    """Base inventory schema."""
    product_id: UUID
    warehouse_id: UUID
    quantity: int = Field(..., ge=0)


class InventoryCreate(InventoryBase):
    """Schema for creating inventory."""
    batch_number: Optional[str] = None
    expiry_date: Optional[datetime] = None


class InventoryUpdate(BaseModel):
    """Schema for updating inventory."""
    quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None


class InventoryResponse(InventoryBase):
    """Schema for inventory response."""
    id: UUID
    reserved_quantity: int
    available_quantity: int
    batch_number: Optional[str] = None
    expiry_date: Optional[datetime] = None
    last_counted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Shipment Schemas =============

class ShipmentItemCreate(BaseModel):
    """Schema for shipment item."""
    product_id: UUID
    quantity: int = Field(..., gt=0)
    unit_price: Optional[float] = None


class ShipmentCreate(BaseModel):
    """Schema for creating shipment."""
    supplier_id: Optional[UUID] = None
    origin_warehouse_id: Optional[UUID] = None
    destination_warehouse_id: Optional[UUID] = None
    shipment_type: str  # inbound, outbound, transfer
    carrier: Optional[str] = None
    estimated_departure: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    items: List[ShipmentItemCreate]
    notes: Optional[str] = None


class ShipmentUpdate(BaseModel):
    """Schema for updating shipment."""
    status: Optional[str] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    notes: Optional[str] = None


class ShipmentResponse(BaseModel):
    """Schema for shipment response."""
    id: UUID
    tracking_number: str
    supplier_id: Optional[UUID] = None
    origin_warehouse_id: Optional[UUID] = None
    destination_warehouse_id: Optional[UUID] = None
    status: str
    shipment_type: str
    carrier: Optional[str] = None
    estimated_departure: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    total_weight: Optional[float] = None
    total_value: Optional[float] = None
    risk_assessment: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Analytics Schemas =============

class DemandForecastRequest(BaseModel):
    """Schema for demand forecast request."""
    product_id: UUID
    warehouse_id: Optional[UUID] = None
    forecast_days: int = Field(default=30, ge=1, le=365)


class DemandForecastResponse(BaseModel):
    """Schema for demand forecast response."""
    product_id: UUID
    warehouse_id: Optional[UUID] = None
    forecasts: List[dict]
    model_version: str
    generated_at: datetime


class AnomalyDetectionRequest(BaseModel):
    """Schema for anomaly detection request."""
    entity_type: str  # product, supplier, shipment
    entity_id: UUID
    time_range_days: int = Field(default=30, ge=1, le=365)


class AnomalyAlertResponse(BaseModel):
    """Schema for anomaly alert response."""
    id: UUID
    alert_type: str
    severity: str
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    description: Optional[str] = None
    anomaly_score: Optional[float] = None
    is_acknowledged: bool
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RouteOptimizationRequest(BaseModel):
    """Schema for route optimization request."""
    origin: dict  # {"latitude": x, "longitude": y}
    destination: dict  # {"latitude": x, "longitude": y}
    waypoints: Optional[List[dict]] = None
    vehicle_capacity: Optional[float] = None
    time_windows: Optional[List[dict]] = None


class RouteOptimizationResponse(BaseModel):
    """Schema for route optimization response."""
    optimized_route: List[dict]
    total_distance_km: float
    estimated_duration_minutes: float
    fuel_estimate_liters: Optional[float] = None
    co2_estimate_kg: Optional[float] = None


# ============= Pagination Schemas =============

class PaginatedResponse(BaseModel):
    """Generic paginated response schema."""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
