"""
SQLAlchemy models for the ChainSense-AI application.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for authentication and authorization."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="user")  # admin, manager, user, viewer
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    api_key = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user")


class Supplier(Base):
    """Supplier/Vendor information."""

    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    risk_score = Column(Float, default=0.0)  # ML-calculated risk score
    reliability_score = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    products = relationship("Product", back_populates="supplier")
    shipments = relationship("Shipment", back_populates="supplier")


class Product(Base):
    """Product/Inventory item."""

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sku = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    unit_price = Column(Float, nullable=False)
    unit_cost = Column(Float)
    weight = Column(Float)  # in kg
    dimensions = Column(JSON)  # {"length": x, "width": y, "height": z}
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"))
    min_stock_level = Column(Integer, default=0)
    max_stock_level = Column(Integer, default=1000)
    reorder_point = Column(Integer, default=100)
    lead_time_days = Column(Integer, default=7)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    supplier = relationship("Supplier", back_populates="products")
    inventory_items = relationship("Inventory", back_populates="product")


class Warehouse(Base):
    """Warehouse/Storage location."""

    __tablename__ = "warehouses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    capacity = Column(Integer)  # Total capacity in units
    current_utilization = Column(Float, default=0.0)  # Percentage
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inventory_items = relationship("Inventory", back_populates="warehouse")


class Inventory(Base):
    """Inventory tracking."""

    __tablename__ = "inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=False)
    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)
    batch_number = Column(String(100))
    expiry_date = Column(DateTime, nullable=True)
    last_counted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="inventory_items")
    warehouse = relationship("Warehouse", back_populates="inventory_items")


class Shipment(Base):
    """Shipment tracking."""

    __tablename__ = "shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tracking_number = Column(String(100), unique=True, nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"))
    origin_warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"))
    destination_warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"))
    status = Column(String(50), default="pending")  # pending, in_transit, delivered, cancelled
    shipment_type = Column(String(50))  # inbound, outbound, transfer
    carrier = Column(String(100))
    estimated_departure = Column(DateTime)
    actual_departure = Column(DateTime)
    estimated_arrival = Column(DateTime)
    actual_arrival = Column(DateTime)
    total_weight = Column(Float)
    total_value = Column(Float)
    route_data = Column(JSON)  # Optimized route information
    risk_assessment = Column(JSON)  # ML-generated risk data
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    supplier = relationship("Supplier", back_populates="shipments")
    items = relationship("ShipmentItem", back_populates="shipment")


class ShipmentItem(Base):
    """Individual items in a shipment."""

    __tablename__ = "shipment_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    shipment = relationship("Shipment", back_populates="items")


class DemandForecast(Base):
    """ML-generated demand forecasts."""

    __tablename__ = "demand_forecasts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"))
    forecast_date = Column(DateTime, nullable=False)
    predicted_demand = Column(Float, nullable=False)
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    model_version = Column(String(50))
    features_used = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnomalyAlert(Base):
    """ML-detected anomalies in supply chain."""

    __tablename__ = "anomaly_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    alert_type = Column(String(100), nullable=False)  # demand_spike, supply_disruption, price_anomaly
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    entity_type = Column(String(50))  # product, supplier, shipment, warehouse
    entity_id = Column(UUID(as_uuid=True))
    description = Column(Text)
    anomaly_score = Column(Float)
    detected_value = Column(Float)
    expected_value = Column(Float)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Audit trail for security and compliance."""

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(String(255))
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    request_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
