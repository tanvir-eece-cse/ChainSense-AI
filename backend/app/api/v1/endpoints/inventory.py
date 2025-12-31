"""
Inventory management endpoints.
"""

from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models import Inventory, Product, Warehouse, User
from app.schemas import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    PaginatedResponse,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def list_inventory(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    warehouse_id: Optional[UUID] = None,
    product_id: Optional[UUID] = None,
    low_stock: bool = False,
) -> dict:
    """List all inventory items with pagination and filtering."""
    query = select(Inventory)
    count_query = select(func.count(Inventory.id))
    
    if warehouse_id:
        query = query.where(Inventory.warehouse_id == warehouse_id)
        count_query = count_query.where(Inventory.warehouse_id == warehouse_id)
    
    if product_id:
        query = query.where(Inventory.product_id == product_id)
        count_query = count_query.where(Inventory.product_id == product_id)
    
    if low_stock:
        # Join with Product to check reorder_point
        query = query.join(Product).where(Inventory.quantity <= Product.reorder_point)
        count_query = count_query.join(Product).where(Inventory.quantity <= Product.reorder_point)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.offset((page - 1) * size).limit(size).order_by(Inventory.updated_at.desc())
    result = await db.execute(query)
    inventory_items = result.scalars().all()
    
    return {
        "items": [InventoryResponse.model_validate(i) for i in inventory_items],
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size,
    }


@router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    inventory_data: InventoryCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Inventory:
    """Create a new inventory record."""
    # Verify product exists
    product_result = await db.execute(
        select(Product).where(Product.id == inventory_data.product_id)
    )
    if not product_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Verify warehouse exists
    warehouse_result = await db.execute(
        select(Warehouse).where(Warehouse.id == inventory_data.warehouse_id)
    )
    if not warehouse_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found",
        )
    
    inventory = Inventory(
        **inventory_data.model_dump(),
        available_quantity=inventory_data.quantity,
    )
    db.add(inventory)
    await db.commit()
    await db.refresh(inventory)
    
    return inventory


@router.get("/{inventory_id}", response_model=InventoryResponse)
async def get_inventory(
    inventory_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Inventory:
    """Get a specific inventory record."""
    result = await db.execute(select(Inventory).where(Inventory.id == inventory_id))
    inventory = result.scalar_one_or_none()
    
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found",
        )
    
    return inventory


@router.patch("/{inventory_id}", response_model=InventoryResponse)
async def update_inventory(
    inventory_id: UUID,
    inventory_data: InventoryUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Inventory:
    """Update an inventory record."""
    result = await db.execute(select(Inventory).where(Inventory.id == inventory_id))
    inventory = result.scalar_one_or_none()
    
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found",
        )
    
    update_data = inventory_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(inventory, field, value)
    
    # Update available quantity
    inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
    
    await db.commit()
    await db.refresh(inventory)
    
    return inventory


@router.post("/{inventory_id}/adjust")
async def adjust_inventory(
    inventory_id: UUID,
    adjustment: int,
    reason: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Adjust inventory quantity with audit trail."""
    result = await db.execute(select(Inventory).where(Inventory.id == inventory_id))
    inventory = result.scalar_one_or_none()
    
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found",
        )
    
    old_quantity = inventory.quantity
    new_quantity = old_quantity + adjustment
    
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adjustment would result in negative inventory",
        )
    
    inventory.quantity = new_quantity
    inventory.available_quantity = new_quantity - inventory.reserved_quantity
    
    await db.commit()
    
    return {
        "inventory_id": str(inventory_id),
        "old_quantity": old_quantity,
        "new_quantity": new_quantity,
        "adjustment": adjustment,
        "reason": reason,
        "adjusted_by": str(current_user.id),
    }


@router.get("/summary/overview")
async def get_inventory_summary(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get inventory summary statistics."""
    # Total items
    total_result = await db.execute(select(func.sum(Inventory.quantity)))
    total_quantity = total_result.scalar() or 0
    
    # Total value (join with products)
    value_result = await db.execute(
        select(func.sum(Inventory.quantity * Product.unit_price))
        .join(Product)
    )
    total_value = value_result.scalar() or 0
    
    # Low stock count
    low_stock_result = await db.execute(
        select(func.count(Inventory.id))
        .join(Product)
        .where(Inventory.quantity <= Product.reorder_point)
    )
    low_stock_count = low_stock_result.scalar() or 0
    
    # Out of stock count
    out_of_stock_result = await db.execute(
        select(func.count(Inventory.id))
        .where(Inventory.quantity == 0)
    )
    out_of_stock_count = out_of_stock_result.scalar() or 0
    
    return {
        "total_quantity": total_quantity,
        "total_value": round(total_value, 2),
        "low_stock_items": low_stock_count,
        "out_of_stock_items": out_of_stock_count,
        "inventory_health": "good" if low_stock_count < 10 else "warning",
    }
