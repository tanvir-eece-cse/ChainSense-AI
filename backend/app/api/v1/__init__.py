"""
API router aggregation for v1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, suppliers, products, inventory, shipments, analytics, health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(shipments.router, prefix="/shipments", tags=["Shipments"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & ML"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
