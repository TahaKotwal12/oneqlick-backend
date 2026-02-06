from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.infra.db.postgres.postgres_config import get_db
from app.services.pricing_service import PricingService
from app.api.schemas.pricing_schemas import (
    PricingConfigResponse,
    PricingConfigUpdateRequest,
    PricingConfigListResponse
)

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.get("/config", response_model=PricingConfigListResponse)
async def get_pricing_config(db: Session = Depends(get_db)):
    """Get all active pricing configuration (public endpoint for frontend)"""
    config = PricingService.get_config(db)
    return {"config": config}


@router.put("/config/{config_key}", response_model=PricingConfigResponse)
async def update_pricing_config(
    config_key: str,
    request: PricingConfigUpdateRequest,
    db: Session = Depends(get_db)
    # TODO: Add admin authentication when ready
    # current_admin: dict = Depends(get_current_admin_user)
):
    """Update pricing configuration (admin only - add auth later)"""
    updated_config = PricingService.update_config(
        db, config_key, Decimal(str(request.value))
    )
    return updated_config
