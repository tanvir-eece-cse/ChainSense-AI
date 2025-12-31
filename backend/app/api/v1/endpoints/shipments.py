"""
Shipment management endpoints.
"""

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models import Shipment, ShipmentItem, Product, User
from app.schemas import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentResponse,
    PaginatedResponse,
)

router = APIRouter()


def generate_tracking_number() -> str:
    """Generate a unique tracking number."""
    import random
    import string
    prefix = "CS"
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}{timestamp}{random_suffix}"


@router.get("", response_model=PaginatedResponse)
async def list_shipments(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    shipment_type: Optional[str] = None,
    supplier_id: Optional[UUID] = None,
) -> dict:
    """List all shipments with pagination and filtering."""
    query = select(Shipment)
    count_query = select(func.count(Shipment.id))
    
    if status:
        query = query.where(Shipment.status == status)
        count_query = count_query.where(Shipment.status == status)
    
    if shipment_type:
        query = query.where(Shipment.shipment_type == shipment_type)
        count_query = count_query.where(Shipment.shipment_type == shipment_type)
    
    if supplier_id:
        query = query.where(Shipment.supplier_id == supplier_id)
        count_query = count_query.where(Shipment.supplier_id == supplier_id)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.offset((page - 1) * size).limit(size).order_by(Shipment.created_at.desc())
    result = await db.execute(query)
    shipments = result.scalars().all()
    
    return {
        "items": [ShipmentResponse.model_validate(s) for s in shipments],
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size,
    }


@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(
    shipment_data: ShipmentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Shipment:
    """Create a new shipment."""
    # Calculate totals
    total_weight = 0
    total_value = 0
    
    for item in shipment_data.items:
        product_result = await db.execute(
            select(Product).where(Product.id == item.product_id)
        )
        product = product_result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found",
            )
        total_weight += (product.weight or 0) * item.quantity
        total_value += (item.unit_price or product.unit_price) * item.quantity
    
    # Create shipment
    shipment = Shipment(
        tracking_number=generate_tracking_number(),
        supplier_id=shipment_data.supplier_id,
        origin_warehouse_id=shipment_data.origin_warehouse_id,
        destination_warehouse_id=shipment_data.destination_warehouse_id,
        shipment_type=shipment_data.shipment_type,
        carrier=shipment_data.carrier,
        estimated_departure=shipment_data.estimated_departure,
        estimated_arrival=shipment_data.estimated_arrival,
        total_weight=total_weight,
        total_value=total_value,
        notes=shipment_data.notes,
    )
    
    db.add(shipment)
    await db.flush()
    
    # Add shipment items
    for item in shipment_data.items:
        shipment_item = ShipmentItem(
            shipment_id=shipment.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        db.add(shipment_item)
    
    await db.commit()
    await db.refresh(shipment)
    
    return shipment


@router.get("/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment(
    shipment_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Shipment:
    """Get a specific shipment by ID."""
    result = await db.execute(select(Shipment).where(Shipment.id == shipment_id))
    shipment = result.scalar_one_or_none()
    
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    
    return shipment


@router.get("/track/{tracking_number}", response_model=ShipmentResponse)
async def track_shipment(
    tracking_number: str,
    db: AsyncSession = Depends(get_db),
) -> Shipment:
    """Track a shipment by tracking number (public endpoint)."""
    result = await db.execute(
        select(Shipment).where(Shipment.tracking_number == tracking_number)
    )
    shipment = result.scalar_one_or_none()
    
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    
    return shipment


@router.patch("/{shipment_id}", response_model=ShipmentResponse)
async def update_shipment(
    shipment_id: UUID,
    shipment_data: ShipmentUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Shipment:
    """Update a shipment."""
    result = await db.execute(select(Shipment).where(Shipment.id == shipment_id))
    shipment = result.scalar_one_or_none()
    
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    
    update_data = shipment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shipment, field, value)
    
    await db.commit()
    await db.refresh(shipment)
    
    return shipment


@router.post("/{shipment_id}/status")
async def update_shipment_status(
    shipment_id: UUID,
    new_status: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Update shipment status with automatic timestamps."""
    valid_statuses = ["pending", "in_transit", "delivered", "cancelled"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}",
        )
    
    result = await db.execute(select(Shipment).where(Shipment.id == shipment_id))
    shipment = result.scalar_one_or_none()
    
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    
    old_status = shipment.status
    shipment.status = new_status
    
    # Update timestamps based on status
    now = datetime.utcnow()
    if new_status == "in_transit" and not shipment.actual_departure:
        shipment.actual_departure = now
    elif new_status == "delivered" and not shipment.actual_arrival:
        shipment.actual_arrival = now
    
    await db.commit()
    
    return {
        "shipment_id": str(shipment_id),
        "old_status": old_status,
        "new_status": new_status,
        "updated_at": now.isoformat(),
    }


@router.get("/summary/overview")
async def get_shipment_summary(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get shipment summary statistics."""
    # Count by status
    status_counts = {}
    for status in ["pending", "in_transit", "delivered", "cancelled"]:
        result = await db.execute(
            select(func.count(Shipment.id)).where(Shipment.status == status)
        )
        status_counts[status] = result.scalar() or 0
    
    # Total value in transit
    value_result = await db.execute(
        select(func.sum(Shipment.total_value))
        .where(Shipment.status == "in_transit")
    )
    value_in_transit = value_result.scalar() or 0
    
    return {
        "total_shipments": sum(status_counts.values()),
        "status_breakdown": status_counts,
        "value_in_transit": round(value_in_transit, 2),
        "on_time_delivery_rate": 0.94,  # Would be calculated from historical data
    }
