from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from uuid import UUID


# ============================================================================
# DELIVERY REQUEST SCHEMAS
# ============================================================================

class DeliveryRestaurantInfo(BaseModel):
    """Restaurant information for delivery"""
    restaurant_id: UUID
    name: str
    address: str
    latitude: Decimal
    longitude: Decimal
    phone: str
    
    class Config:
        from_attributes = True


class DeliveryCustomerInfo(BaseModel):
    """Customer information for delivery"""
    customer_id: UUID
    name: str
    phone: str
    address: str
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


class DeliveryRequestResponse(BaseModel):
    """Delivery request response"""
    order_id: UUID
    order_number: str
    amount: Decimal
    restaurant: DeliveryRestaurantInfo
    customer: DeliveryCustomerInfo
    payment_type: str
    distance: Optional[float] = None  # in km
    estimated_time: Optional[int] = None  # in minutes
    created_at: datetime
    
    class Config:
        from_attributes = True


class DeliveryRequestListResponse(BaseModel):
    """List of delivery requests"""
    requests: List[DeliveryRequestResponse]
    total_count: int


class AcceptDeliveryResponse(BaseModel):
    """Response after accepting delivery"""
    order_id: UUID
    order_number: str
    status: str
    restaurant: DeliveryRestaurantInfo
    customer: DeliveryCustomerInfo
    amount: Decimal
    accepted_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# DELIVERY STATUS SCHEMAS
# ============================================================================

class UpdateDeliveryStatusRequest(BaseModel):
    """Request to update delivery status"""
    status: str = Field(..., description="New delivery status")
    latitude: Optional[Decimal] = Field(None, description="Current latitude")
    longitude: Optional[Decimal] = Field(None, description="Current longitude")
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['picked_up', 'delivered']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v


class UpdateLocationRequest(BaseModel):
    """Request to update current location"""
    latitude: Decimal = Field(..., ge=-90, le=90)
    longitude: Decimal = Field(..., ge=-180, le=180)


class UpdateLocationResponse(BaseModel):
    """Response after updating location"""
    updated: bool
    latitude: Decimal
    longitude: Decimal
    updated_at: datetime


class UpdateAvailabilityRequest(BaseModel):
    """Request to toggle online/offline status"""
    is_online: bool


class UpdateAvailabilityResponse(BaseModel):
    """Response after updating availability"""
    is_online: bool
    updated_at: datetime


# ============================================================================
# ACTIVE ORDERS SCHEMAS
# ============================================================================

class ActiveDeliveryResponse(BaseModel):
    """Active delivery order response"""
    order_id: UUID
    order_number: str
    status: str
    amount: Decimal
    restaurant: DeliveryRestaurantInfo
    customer: DeliveryCustomerInfo
    payment_type: str
    picked_up_at: Optional[datetime] = None
    estimated_delivery_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ActiveDeliveryListResponse(BaseModel):
    """List of active deliveries"""
    active_orders: List[ActiveDeliveryResponse]
    total_count: int


# ============================================================================
# DELIVERY PARTNER PROFILE SCHEMAS
# ============================================================================

class DeliveryPartnerProfileResponse(BaseModel):
    """Delivery partner profile response"""
    delivery_partner_id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    profile_image: Optional[str] = None
    vehicle_type: str
    vehicle_number: str
    license_number: str
    current_latitude: Optional[Decimal] = None
    current_longitude: Optional[Decimal] = None
    availability_status: str
    rating: Optional[Decimal] = None
    total_ratings: Optional[int] = 0
    total_deliveries: Optional[int] = 0
    is_verified: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


class UpdateDeliveryPartnerProfileRequest(BaseModel):
    """Request to update delivery partner profile"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=50)
    
    @validator('vehicle_type')
    def validate_vehicle_type(cls, v):
        if v is not None:
            allowed_types = ['bicycle', 'motorcycle', 'car']
            if v not in allowed_types:
                raise ValueError(f'Vehicle type must be one of: {", ".join(allowed_types)}')
        return v


class UploadDocumentsResponse(BaseModel):
    """Response after uploading documents"""
    document_urls: List[str]
    uploaded_count: int


# ============================================================================
# EARNINGS & STATISTICS SCHEMAS
# ============================================================================

class EarningsBreakdown(BaseModel):
    """Daily earnings breakdown"""
    date: str
    amount: Decimal
    deliveries: int


class DeliveryEarningsResponse(BaseModel):
    """Delivery partner earnings response"""
    total_amount: Decimal
    total_deliveries: int
    tips: Decimal
    bonus: Decimal
    breakdown: List[EarningsBreakdown]
    period: str  # 'today', 'week', 'month'


class DeliveryStatsResponse(BaseModel):
    """Delivery partner statistics"""
    total_deliveries: int
    success_rate: float  # percentage
    avg_rating: Optional[Decimal] = None
    total_earnings: Decimal
    today_deliveries: int
    today_earnings: Decimal
    this_week_deliveries: int
    this_week_earnings: Decimal
    this_month_deliveries: int
    this_month_earnings: Decimal


class TransactionResponse(BaseModel):
    """Transaction response"""
    transaction_id: UUID
    order_id: UUID
    order_number: str
    amount: Decimal
    type: str  # 'delivery_fee', 'tip', 'bonus'
    date: datetime
    
    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    """List of transactions"""
    transactions: List[TransactionResponse]
    total_count: int
    has_more: bool


class PerformanceMetricsResponse(BaseModel):
    """Performance metrics for delivery partner"""
    on_time_rate: float  # percentage
    customer_ratings: Optional[Decimal] = None
    total_distance_covered: float  # in km
    avg_delivery_time: int  # in minutes
    total_orders_completed: int
    total_orders_cancelled: int
    acceptance_rate: float  # percentage
