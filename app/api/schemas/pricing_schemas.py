from pydantic import BaseModel
from decimal import Decimal
from typing import Dict, Optional
from uuid import UUID


class PricingConfigResponse(BaseModel):
    config_id: str
    config_key: str
    config_value: Decimal
    config_type: str
    description: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True


class PricingConfigUpdateRequest(BaseModel):
    value: Decimal


class PricingConfigListResponse(BaseModel):
    config: Dict[str, Decimal]


class OrderPreviewRequest(BaseModel):
    cart_id: UUID
    address_id: UUID
    coupon_code: Optional[str] = None


class OrderPreviewResponse(BaseModel):
    subtotal: float
    tax_amount: float
    delivery_fee: float
    platform_fee: float
    discount_amount: float
    total_amount: float
    distance_km: float
