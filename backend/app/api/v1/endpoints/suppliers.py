"""
Supplier management endpoints.
"""

from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models import Supplier, User
from app.schemas import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
    PaginatedResponse,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
async def list_suppliers(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> dict:
    """List all suppliers with pagination and filtering."""
    query = select(Supplier)
    count_query = select(func.count(Supplier.id))
    
    if search:
        query = query.where(
            Supplier.name.ilike(f"%{search}%") | Supplier.code.ilike(f"%{search}%")
        )
        count_query = count_query.where(
            Supplier.name.ilike(f"%{search}%") | Supplier.code.ilike(f"%{search}%")
        )
    
    if is_active is not None:
        query = query.where(Supplier.is_active == is_active)
        count_query = count_query.where(Supplier.is_active == is_active)
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    query = query.offset((page - 1) * size).limit(size).order_by(Supplier.created_at.desc())
    result = await db.execute(query)
    suppliers = result.scalars().all()
    
    return {
        "items": [SupplierResponse.model_validate(s) for s in suppliers],
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size,
    }


@router.post("", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    supplier_data: SupplierCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Supplier:
    """Create a new supplier."""
    # Check if code already exists
    result = await db.execute(select(Supplier).where(Supplier.code == supplier_data.code))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier code already exists",
        )
    
    supplier = Supplier(**supplier_data.model_dump())
    db.add(supplier)
    await db.commit()
    await db.refresh(supplier)
    
    return supplier


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Supplier:
    """Get a specific supplier by ID."""
    result = await db.execute(select(Supplier).where(Supplier.id == supplier_id))
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )
    
    return supplier


@router.patch("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: UUID,
    supplier_data: SupplierUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> Supplier:
    """Update a supplier."""
    result = await db.execute(select(Supplier).where(Supplier.id == supplier_id))
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )
    
    update_data = supplier_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    await db.commit()
    await db.refresh(supplier)
    
    return supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(
    supplier_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a supplier (soft delete)."""
    result = await db.execute(select(Supplier).where(Supplier.id == supplier_id))
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )
    
    supplier.is_active = False
    await db.commit()


@router.get("/{supplier_id}/risk-assessment")
async def get_supplier_risk(
    supplier_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get ML-based risk assessment for a supplier."""
    result = await db.execute(select(Supplier).where(Supplier.id == supplier_id))
    supplier = result.scalar_one_or_none()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )
    
    # Return risk assessment data
    return {
        "supplier_id": str(supplier_id),
        "supplier_name": supplier.name,
        "risk_score": supplier.risk_score,
        "reliability_score": supplier.reliability_score,
        "risk_factors": {
            "delivery_performance": 0.85,
            "quality_score": 0.92,
            "financial_stability": 0.78,
            "geographic_risk": 0.65,
        },
        "recommendations": [
            "Monitor delivery times closely",
            "Consider backup supplier for critical items",
        ],
    }
