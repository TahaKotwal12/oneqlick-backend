from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.utils.enums import OrderStatus, PaymentStatus, PaymentMethod


# ============================================
# REQUEST SCHEMAS
# ============================================

class OrderCreateRequest(BaseModel):
    """Request schema for creating an order"""
    cart_id: UUID = Field(..., description="Cart ID to create order from")
    address_id: UUID = Field(..., description="Delivery address ID")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    coupon_code: Optional[str] = Field(None, max_length=50, description="Coupon code to apply")
    special_instructions: Optional[str] = Field(None, max_length=500, description="Special instructions for the order")
    
    class Config:
        json_schema_extra = {
            "example": {
                "cart_id": "123e4567-e89b-12d3-a456-426614174000",
                "address_id": "123e4567-e89b-12d3-a456-426614174001",
                "payment_method": "cash",
                "coupon_code": "SAVE20",
                "special_instructions": "Please ring the doorbell"
            }
        }


class OrderValidateRequest(BaseModel):
    """Request schema for validating an order before placement"""
    cart_id: UUID = Field(..., description="Cart ID to validate")
    address_id: UUID = Field(..., description="Delivery address ID")
    coupon_code: Optional[str] = Field(None, max_length=50, description="Coupon code to validate")


class OrderCancelRequest(BaseModel):
    """Request schema for cancelling an order"""
    cancellation_reason: str = Field(..., min_length=10, max_length=500, description="Reason for cancellation")


class OrderRatingRequest(BaseModel):
    """Request schema for rating an order"""
    restaurant_rating: int = Field(..., ge=1, le=5, description="Restaurant rating (1-5)")
    delivery_rating: Optional[int] = Field(None, ge=1, le=5, description="Delivery partner rating (1-5)")
    review_text: Optional[str] = Field(None, max_length=1000, description="Review text")
    food_ratings: Optional[List[Dict[str, Any]]] = Field(None, description="Individual food item ratings")
    
    @validator('restaurant_rating', 'delivery_rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v


class OrderAcceptRequest(BaseModel):
    """Request schema for restaurant accepting an order"""
    estimated_prep_time: int = Field(..., ge=5, le=180, description="Estimated preparation time in minutes")


class OrderRejectRequest(BaseModel):
    """Request schema for restaurant rejecting an order"""
    rejection_reason: str = Field(..., min_length=10, max_length=500, description="Reason for rejection")


class OrderStatusUpdateRequest(BaseModel):
    """Request schema for updating order status"""
    status: OrderStatus = Field(..., description="New order status")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")


class DeliveryLocationUpdateRequest(BaseModel):
    """Request schema for updating delivery partner location"""
    latitude: float = Field(..., ge=-90, le=90, description="Current latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Current longitude")


class DeliveryCompleteRequest(BaseModel):
    """Request schema for marking delivery complete"""
    otp_code: Optional[str] = Field(None, max_length=6, description="OTP code for verification")
    delivery_photo: Optional[str] = Field(None, description="Proof of delivery photo URL")
    signature: Optional[str] = Field(None, description="Customer signature data")


class PickupCompleteRequest(BaseModel):
    """Request schema for marking pickup complete"""
    pickup_time: datetime = Field(..., description="Actual pickup time")
    pickup_photo: Optional[str] = Field(None, description="Photo of picked up order")


# ============================================
# RESPONSE SCHEMAS
# ============================================

class AddressResponse(BaseModel):
    """Response schema for address"""
    address_id: UUID
    title: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    postal_code: str
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v) if v else None
        }


class RestaurantBasicResponse(BaseModel):
    """Basic restaurant information for order"""
    restaurant_id: UUID
    name: str
    phone: str
    image: Optional[str]
    address_line1: str
    city: str
    
    class Config:
        from_attributes = True


class DeliveryPartnerResponse(BaseModel):
    """Delivery partner information"""
    user_id: UUID
    first_name: str
    last_name: str
    phone: str
    profile_image: Optional[str]
    vehicle_type: Optional[str]
    vehicle_number: Optional[str]
    rating: Optional[Decimal]
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v) if v else None
        }


class OrderItemResponse(BaseModel):
    """Response schema for order item"""
    order_item_id: UUID
    food_item_id: UUID
    food_item_name: str
    food_item_image: Optional[str]
    variant_id: Optional[UUID]
    variant_name: Optional[str]
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    special_instructions: Optional[str]
    is_veg: bool
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class OrderTrackingResponse(BaseModel):
    """Response schema for order tracking"""
    order_tracking_id: UUID
    status: OrderStatus
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v) if v else None
        }


class PriceBreakdownResponse(BaseModel):
    """Response schema for price breakdown"""
    subtotal: Decimal
    tax_amount: Decimal
    delivery_fee: Decimal
    discount_amount: Decimal
    platform_fee: Optional[Decimal]
    total_amount: Decimal
    coupon_applied: Optional[str]
    coupon_discount: Optional[Decimal]
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class OrderResponse(BaseModel):
    """Response schema for order"""
    order_id: UUID
    order_number: str
    customer_id: UUID
    restaurant_id: UUID
    restaurant: RestaurantBasicResponse
    delivery_partner_id: Optional[UUID]
    delivery_address_id: UUID
    delivery_address: AddressResponse
    subtotal: Decimal
    tax_amount: Decimal
    delivery_fee: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    payment_id: Optional[str]
    order_status: OrderStatus
    estimated_delivery_time: Optional[datetime]
    actual_delivery_time: Optional[datetime]
    special_instructions: Optional[str]
    cancellation_reason: Optional[str]
    rating: Optional[int]
    review: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class OrderDetailResponse(OrderResponse):
    """Detailed order response with items and tracking"""
    items: List[OrderItemResponse] = []
    delivery_partner: Optional[DeliveryPartnerResponse] = None
    tracking: List[OrderTrackingResponse] = []
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class MyOrdersResponse(BaseModel):
    """Response schema for my orders list"""
    orders: List[OrderResponse]
    total_count: int
    has_more: bool
    
    class Config:
        from_attributes = True


class OrderTrackingDetailResponse(BaseModel):
    """Response schema for real-time order tracking"""
    order_id: UUID
    order_number: str
    order_status: OrderStatus
    estimated_delivery_time: Optional[datetime]
    restaurant: RestaurantBasicResponse
    delivery_address: AddressResponse
    delivery_partner: Optional[DeliveryPartnerResponse]
    current_location: Optional[Dict[str, float]]  # {latitude, longitude}
    tracking_history: List[OrderTrackingResponse]
    
    class Config:
        from_attributes = True


# ============================================
# RESTAURANT OWNER SCHEMAS
# ============================================

class RestaurantOrderResponse(BaseModel):
    """Response schema for restaurant order view"""
    order_id: UUID
    order_number: str
    customer_name: str
    customer_phone: str
    items: List[OrderItemResponse]
    subtotal: Decimal
    total_amount: Decimal
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    order_status: OrderStatus
    special_instructions: Optional[str]
    estimated_delivery_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class RestaurantOrdersResponse(BaseModel):
    """Response schema for restaurant orders list"""
    orders: List[RestaurantOrderResponse]
    total_count: int
    has_more: bool


class RestaurantAnalyticsResponse(BaseModel):
    """Response schema for restaurant analytics"""
    total_orders: int
    total_revenue: Decimal
    avg_order_value: Decimal
    pending_orders: int
    completed_orders: int
    cancelled_orders: int
    popular_items: List[Dict[str, Any]]
    revenue_by_date: List[Dict[str, Any]]
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# ============================================
# DELIVERY PARTNER SCHEMAS
# ============================================

class DeliveryOrderResponse(BaseModel):
    """Response schema for delivery partner order view"""
    order_id: UUID
    order_number: str
    restaurant: RestaurantBasicResponse
    delivery_address: AddressResponse
    customer_name: str
    customer_phone: str
    total_amount: Decimal
    payment_method: PaymentMethod
    order_status: OrderStatus
    estimated_delivery_time: Optional[datetime]
    distance_km: Optional[float]
    delivery_fee: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class AvailableDeliveriesResponse(BaseModel):
    """Response schema for available deliveries"""
    deliveries: List[DeliveryOrderResponse]
    total_count: int


class DeliveryEarningsResponse(BaseModel):
    """Response schema for delivery earnings"""
    total_earnings: Decimal
    completed_deliveries: int
    avg_per_delivery: Decimal
    earnings_by_date: List[Dict[str, Any]]
    total_distance_km: float
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


# ============================================
# ADMIN SCHEMAS
# ============================================

class AdminOrderResponse(OrderDetailResponse):
    """Response schema for admin order view"""
    customer_name: str
    customer_email: str
    customer_phone: str
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class AdminOrdersResponse(BaseModel):
    """Response schema for admin orders list"""
    orders: List[AdminOrderResponse]
    total_count: int
    total_orders_completed: int  # Add this
    page: int                   # Add this
    page_size: int              # Add this
    total_pages: int            # Add this
    has_more: bool


class AdminAnalyticsResponse(BaseModel):
    """Response schema for platform-wide analytics"""
    total_orders: int
    total_revenue: Decimal
    avg_order_value: Decimal
    total_customers: int
    total_restaurants: int
    total_delivery_partners: int
    orders_by_status: Dict[str, int]
    revenue_by_date: List[Dict[str, Any]]
    top_restaurants: List[Dict[str, Any]]
    top_customers: List[Dict[str, Any]]
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class AdminInterventionRequest(BaseModel):
    """Request schema for admin intervention"""
    action: str = Field(..., description="Action to perform: cancel, reassign_delivery, refund")
    reason: str = Field(..., min_length=10, max_length=500, description="Reason for intervention")
    new_delivery_partner_id: Optional[UUID] = Field(None, description="New delivery partner ID for reassignment")
    
    @validator('action')
    def validate_action(cls, v):
        valid_actions = ['cancel', 'reassign_delivery', 'refund']
        if v not in valid_actions:
            raise ValueError(f'Action must be one of: {", ".join(valid_actions)}')
        return v
