from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.utils.enums import CouponType


# Request Schemas
class ValidateCouponRequest(BaseModel):
    """Request schema for validating a coupon."""
    coupon_code: str = Field(..., description="Coupon code to validate")
    cart_total: Decimal = Field(..., gt=0, description="Cart subtotal amount")
    restaurant_id: Optional[UUID] = Field(None, description="Restaurant ID if applicable")

    class Config:
        json_schema_extra = {
            "example": {
                "coupon_code": "SAVE20",
                "cart_total": 360.00,
                "restaurant_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class ApplyCouponRequest(BaseModel):
    """Request schema for applying a coupon to cart."""
    coupon_code: str = Field(..., description="Coupon code to apply")
    cart_total: Decimal = Field(..., gt=0, description="Cart subtotal amount")
    restaurant_id: Optional[UUID] = Field(None, description="Restaurant ID")

    class Config:
        json_schema_extra = {
            "example": {
                "coupon_code": "SAVE20",
                "cart_total": 360.00,
                "restaurant_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


# Response Schemas
class CouponResponse(BaseModel):
    """Response schema for a single coupon."""
    coupon_id: UUID
    code: str
    title: str
    description: Optional[str]
    coupon_type: CouponType
    discount_value: Decimal
    min_order_amount: Decimal
    max_discount_amount: Optional[Decimal]
    usage_limit: Optional[int]
    used_count: int
    valid_from: datetime
    valid_until: datetime
    is_active: bool
    created_at: datetime
    
    # Computed fields
    is_expired: bool = Field(default=False, description="Whether coupon has expired")
    is_available: bool = Field(default=True, description="Whether coupon is available for use")
    usage_remaining: Optional[int] = Field(None, description="Remaining usage count")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "coupon_id": "123e4567-e89b-12d3-a456-426614174000",
                "code": "SAVE20",
                "title": "Save 20% on orders above ₹300",
                "description": "Get 20% discount on your order",
                "coupon_type": "percentage",
                "discount_value": 20.00,
                "min_order_amount": 300.00,
                "max_discount_amount": 100.00,
                "usage_limit": 1000,
                "used_count": 245,
                "valid_from": "2026-01-01T00:00:00Z",
                "valid_until": "2026-01-31T23:59:59Z",
                "is_active": True,
                "created_at": "2026-01-01T00:00:00Z",
                "is_expired": False,
                "is_available": True,
                "usage_remaining": 755
            }
        }


class CouponListResponse(BaseModel):
    """Response schema for list of coupons."""
    coupons: List[CouponResponse]
    total_count: int
    available_count: int = Field(description="Number of coupons user can use")

    class Config:
        json_schema_extra = {
            "example": {
                "coupons": [],
                "total_count": 5,
                "available_count": 3
            }
        }


class ValidateCouponResponse(BaseModel):
    """Response schema for coupon validation."""
    is_valid: bool
    coupon: Optional[CouponResponse] = None
    discount_amount: Decimal = Field(default=0, description="Calculated discount amount")
    final_amount: Decimal = Field(description="Final amount after discount")
    error_message: Optional[str] = Field(None, description="Error message if invalid")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_valid": True,
                "coupon": {
                    "code": "SAVE20",
                    "title": "Save 20% on orders above ₹300",
                    "coupon_type": "percentage",
                    "discount_value": 20.00
                },
                "discount_amount": 72.00,
                "final_amount": 288.00,
                "error_message": None
            }
        }


class ApplyCouponResponse(BaseModel):
    """Response schema for applying coupon."""
    success: bool
    message: str
    coupon_code: str
    discount_amount: Decimal
    final_amount: Decimal

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Coupon applied successfully",
                "coupon_code": "SAVE20",
                "discount_amount": 72.00,
                "final_amount": 288.00
            }
        }


class RestaurantOfferResponse(BaseModel):
    """Response schema for restaurant offer."""
    offer_id: UUID
    restaurant_id: UUID
    title: str
    description: Optional[str]
    discount_type: str  # 'percentage', 'fixed_amount', 'free_delivery'
    discount_value: Decimal
    min_order_amount: Optional[Decimal]
    max_discount_amount: Optional[Decimal]
    valid_from: datetime
    valid_until: datetime
    is_active: bool
    created_at: datetime
    
    # Computed fields
    is_expired: bool = Field(default=False, description="Whether offer has expired")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "offer_id": "123e4567-e89b-12d3-a456-426614174000",
                "restaurant_id": "123e4567-e89b-12d3-a456-426614174001",
                "title": "Free Delivery on orders above ₹200",
                "description": "Get free delivery",
                "discount_type": "free_delivery",
                "discount_value": 0.00,
                "min_order_amount": 200.00,
                "max_discount_amount": None,
                "valid_from": "2026-01-01T00:00:00Z",
                "valid_until": "2026-01-31T23:59:59Z",
                "is_active": True,
                "created_at": "2026-01-01T00:00:00Z",
                "is_expired": False
            }
        }


class OffersListResponse(BaseModel):
    """Response schema for list of offers."""
    offers: List[RestaurantOfferResponse]
    total_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "offers": [],
                "total_count": 3
            }
        }


class CouponUsageResponse(BaseModel):
    """Response schema for coupon usage history."""
    user_coupon_usage_id: UUID
    coupon_code: str
    coupon_title: str
    order_id: UUID
    order_number: str
    discount_amount: Decimal
    used_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "user_coupon_usage_id": "123e4567-e89b-12d3-a456-426614174000",
                "coupon_code": "SAVE20",
                "coupon_title": "Save 20% on orders above ₹300",
                "order_id": "123e4567-e89b-12d3-a456-426614174001",
                "order_number": "OQ20260103001",
                "discount_amount": 72.00,
                "used_at": "2026-01-03T12:00:00Z"
            }
        }


class CouponUsageListResponse(BaseModel):
    """Response schema for coupon usage history list."""
    usage_history: List[CouponUsageResponse]
    total_count: int
    total_savings: Decimal = Field(description="Total amount saved using coupons")

    class Config:
        json_schema_extra = {
            "example": {
                "usage_history": [],
                "total_count": 5,
                "total_savings": 350.00
            }
        }


class CarouselCouponResponse(BaseModel):
    """Response schema for carousel coupon display."""
    coupon_id: UUID
    code: str
    title: str
    description: Optional[str]
    coupon_type: CouponType
    discount_value: Decimal
    min_order_amount: Decimal
    max_discount_amount: Optional[Decimal]
    
    # Carousel-specific fields
    carousel_title: Optional[str]
    carousel_subtitle: Optional[str]
    carousel_badge: Optional[str]
    carousel_icon: Optional[str]
    carousel_gradient_start: str
    carousel_gradient_middle: str
    carousel_gradient_end: str
    carousel_action_text: str
    carousel_priority: int
    
    # Computed fields
    is_expired: bool = Field(default=False, description="Whether coupon has expired")
    discount_display: str = Field(default="", description="Formatted discount display")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "coupon_id": "123e4567-e89b-12d3-a456-426614174000",
                "code": "MEGA60",
                "title": "Save 60% on orders above ₹199",
                "description": "On your first 3 orders above ₹199",
                "coupon_type": "percentage",
                "discount_value": 60.00,
                "min_order_amount": 199.00,
                "max_discount_amount": 100.00,
                "carousel_title": "MEGA SALE",
                "carousel_subtitle": "Up to 60% OFF",
                "carousel_badge": "LIMITED TIME",
                "carousel_icon": "fire",
                "carousel_gradient_start": "#4F46E5",
                "carousel_gradient_middle": "#6366F1",
                "carousel_gradient_end": "#818CF8",
                "carousel_action_text": "Order Now",
                "carousel_priority": 1,
                "is_expired": False,
                "discount_display": "60%"
            }
        }


class CarouselCouponsListResponse(BaseModel):
    """Response schema for carousel coupons list."""
    coupons: List[CarouselCouponResponse]
    total_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "coupons": [],
                "total_count": 5
            }
        }


# Admin Schemas
class CreateCouponRequest(BaseModel):
    """Request schema for creating a coupon (admin only)."""
    code: str = Field(..., min_length=3, max_length=50, description="Unique coupon code")
    title: str = Field(..., min_length=3, max_length=255, description="Coupon title")
    description: Optional[str] = Field(None, description="Coupon description")
    coupon_type: CouponType = Field(..., description="Type of coupon")
    discount_value: Decimal = Field(..., gt=0, description="Discount value")
    min_order_amount: Decimal = Field(..., ge=0, description="Minimum order amount")
    max_discount_amount: Optional[Decimal] = Field(None, ge=0, description="Maximum discount amount")
    usage_limit: Optional[int] = Field(None, gt=0, description="Maximum usage limit")
    valid_from: datetime = Field(..., description="Coupon valid from date")
    valid_until: datetime = Field(..., description="Coupon valid until date")
    is_active: bool = Field(default=True, description="Whether coupon is active")
    
    # Carousel fields
    show_in_carousel: bool = Field(default=False, description="Show in home carousel")
    carousel_priority: int = Field(default=0, ge=0, le=100, description="Carousel display priority")
    carousel_title: Optional[str] = Field(None, max_length=100, description="Carousel title")
    carousel_subtitle: Optional[str] = Field(None, max_length=100, description="Carousel subtitle")
    carousel_badge: Optional[str] = Field(None, max_length=50, description="Carousel badge text")
    carousel_icon: Optional[str] = Field(None, max_length=50, description="Carousel icon name")
    carousel_gradient_start: str = Field(default="#4F46E5", description="Gradient start color")
    carousel_gradient_middle: str = Field(default="#6366F1", description="Gradient middle color")
    carousel_gradient_end: str = Field(default="#818CF8", description="Gradient end color")
    carousel_action_text: str = Field(default="Order Now", max_length=50, description="Action button text")

    @validator('code')
    def validate_code(cls, v):
        if not v.isupper() or not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Code must be uppercase alphanumeric (can include _ and -)')
        return v

    @validator('valid_until')
    def validate_dates(cls, v, values):
        if 'valid_from' in values and v <= values['valid_from']:
            raise ValueError('valid_until must be after valid_from')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "code": "MEGA50",
                "title": "50% OFF on first order",
                "description": "Get 50% discount on your first order above ₹299",
                "coupon_type": "percentage",
                "discount_value": 50.00,
                "min_order_amount": 299.00,
                "max_discount_amount": 150.00,
                "usage_limit": 1000,
                "valid_from": "2026-02-06T00:00:00Z",
                "valid_until": "2026-03-06T23:59:59Z",
                "is_active": True,
                "show_in_carousel": True,
                "carousel_priority": 10,
                "carousel_title": "MEGA SALE",
                "carousel_subtitle": "Up to 50% OFF",
                "carousel_badge": "LIMITED TIME",
                "carousel_icon": "fire",
                "carousel_gradient_start": "#4F46E5",
                "carousel_gradient_middle": "#6366F1",
                "carousel_gradient_end": "#818CF8",
                "carousel_action_text": "Order Now"
            }
        }


class UpdateCouponRequest(BaseModel):
    """Request schema for updating a coupon (admin only)."""
    code: Optional[str] = Field(None, min_length=3, max_length=50)
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    coupon_type: Optional[CouponType] = None
    discount_value: Optional[Decimal] = Field(None, gt=0)
    min_order_amount: Optional[Decimal] = Field(None, ge=0)
    max_discount_amount: Optional[Decimal] = Field(None, ge=0)
    usage_limit: Optional[int] = Field(None, gt=0)
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    is_active: Optional[bool] = None
    
    # Carousel fields
    show_in_carousel: Optional[bool] = None
    carousel_priority: Optional[int] = Field(None, ge=0, le=100)
    carousel_title: Optional[str] = Field(None, max_length=100)
    carousel_subtitle: Optional[str] = Field(None, max_length=100)
    carousel_badge: Optional[str] = Field(None, max_length=50)
    carousel_icon: Optional[str] = Field(None, max_length=50)
    carousel_gradient_start: Optional[str] = None
    carousel_gradient_middle: Optional[str] = None
    carousel_gradient_end: Optional[str] = None
    carousel_action_text: Optional[str] = Field(None, max_length=50)

    @validator('code')
    def validate_code(cls, v):
        if v and (not v.isupper() or not v.replace('_', '').replace('-', '').isalnum()):
            raise ValueError('Code must be uppercase alphanumeric (can include _ and -)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "carousel_priority": 20,
                "is_active": False
            }
        }


class AdminCouponResponse(BaseModel):
    """Response schema for admin coupon operations."""
    coupon_id: UUID
    code: str
    title: str
    description: Optional[str]
    coupon_type: CouponType
    discount_value: Decimal
    min_order_amount: Decimal
    max_discount_amount: Optional[Decimal]
    usage_limit: Optional[int]
    used_count: int
    valid_from: datetime
    valid_until: datetime
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None  # Made optional for existing coupons
    
    # Carousel fields
    show_in_carousel: bool
    carousel_priority: int
    carousel_title: Optional[str]
    carousel_subtitle: Optional[str]
    carousel_badge: Optional[str]
    carousel_icon: Optional[str]
    carousel_gradient_start: str
    carousel_gradient_middle: str
    carousel_gradient_end: str
    carousel_action_text: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "coupon_id": "123e4567-e89b-12d3-a456-426614174000",
                "code": "MEGA50",
                "title": "50% OFF on first order",
                "description": "Get 50% discount",
                "coupon_type": "percentage",
                "discount_value": 50.00,
                "min_order_amount": 299.00,
                "max_discount_amount": 150.00,
                "usage_limit": 1000,
                "used_count": 245,
                "valid_from": "2026-02-06T00:00:00Z",
                "valid_until": "2026-03-06T23:59:59Z",
                "is_active": True,
                "created_at": "2026-02-06T00:00:00Z",
                "updated_at": None,
                "show_in_carousel": True,
                "carousel_priority": 10,
                "carousel_title": "MEGA SALE",
                "carousel_subtitle": "Up to 50% OFF",
                "carousel_badge": "LIMITED TIME",
                "carousel_icon": "fire",
                "carousel_gradient_start": "#4F46E5",
                "carousel_gradient_middle": "#6366F1",
                "carousel_gradient_end": "#818CF8",
                "carousel_action_text": "Order Now"
            }
        }


class AdminCouponListResponse(BaseModel):
    """Response schema for admin coupon list."""
    coupons: List[AdminCouponResponse]
    total_count: int
    page: int
    limit: int
    has_more: bool

    class Config:
        json_schema_extra = {
            "example": {
                "coupons": [],
                "total_count": 25,
                "page": 1,
                "limit": 50,
                "has_more": False
            }
        }


