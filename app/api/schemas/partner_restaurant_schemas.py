from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from uuid import UUID


# ============================================================================
# ORDER MANAGEMENT SCHEMAS
# ============================================================================

class OrderItemResponse(BaseModel):
    """Single item in an order"""
    food_item_id: UUID
    name: str
    quantity: int
    price: Decimal
    customizations: Optional[List[str]] = []
    addons: Optional[List[str]] = []
    
    class Config:
        from_attributes = True


class DeliveryAddressResponse(BaseModel):
    """Delivery address details"""
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: str
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


class RestaurantOrderResponse(BaseModel):
    """Order response for restaurant owner"""
    order_id: UUID
    order_number: str
    customer_name: str
    customer_phone: str
    total_amount: Decimal
    subtotal: Decimal
    tax_amount: Decimal
    delivery_fee: Decimal
    discount_amount: Decimal
    order_status: str
    payment_status: str
    payment_method: str
    created_at: datetime
    estimated_delivery_time: Optional[datetime] = None
    special_instructions: Optional[str] = None
    items: List[OrderItemResponse]
    delivery_address: Optional[DeliveryAddressResponse] = None
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """List of orders with pagination"""
    orders: List[RestaurantOrderResponse]
    total_count: int
    has_more: bool


class UpdateOrderStatusRequest(BaseModel):
    """Request to update order status"""
    status: str = Field(..., description="New order status")
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['preparing', 'ready_for_pickup', 'rejected']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v


class AddOrderNoteRequest(BaseModel):
    """Request to add note to order"""
    note: str = Field(..., min_length=1, max_length=500)


class OrderNoteResponse(BaseModel):
    """Order note response"""
    note_id: UUID
    note: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class RestaurantStatsResponse(BaseModel):
    """Restaurant statistics"""
    today_orders: int
    pending_orders: int
    revenue_today: Decimal
    avg_preparation_time: int  # in minutes
    total_orders_this_month: int
    revenue_this_month: Decimal


# ============================================================================
# MENU MANAGEMENT SCHEMAS
# ============================================================================

class MenuItemResponse(BaseModel):
    """Menu item response"""
    food_item_id: UUID
    name: str
    description: Optional[str] = None
    price: Decimal
    discount_price: Optional[Decimal] = None
    category_id: Optional[UUID] = None
    category_name: Optional[str] = None
    image: Optional[str] = None
    is_veg: bool
    is_available: bool = True
    ingredients: Optional[str] = None
    allergens: Optional[str] = None
    prep_time: Optional[int] = None
    calories: Optional[int] = None
    rating: Optional[Decimal] = None
    total_ratings: Optional[int] = 0
    is_popular: bool = False
    is_recommended: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MenuListResponse(BaseModel):
    """List of menu items"""
    items: List[MenuItemResponse]
    total_count: int


class CreateMenuItemRequest(BaseModel):
    """Request to create menu item"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., gt=0, description="Price must be greater than 0")
    category_id: UUID
    is_veg: bool = True
    image_url: Optional[str] = Field(None, max_length=500)
    ingredients: Optional[str] = Field(None, max_length=500)
    allergens: Optional[str] = Field(None, max_length=500)
    prep_time: Optional[int] = Field(None, ge=0, description="Preparation time in minutes")
    calories: Optional[int] = Field(None, ge=0)
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v


class UpdateMenuItemRequest(BaseModel):
    """Request to update menu item"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, gt=0)
    image_url: Optional[str] = Field(None, max_length=500)
    ingredients: Optional[str] = Field(None, max_length=500)
    allergens: Optional[str] = Field(None, max_length=500)
    prep_time: Optional[int] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None


class UpdateItemAvailabilityRequest(BaseModel):
    """Request to update item availability"""
    is_available: bool


class BulkUpdateMenuItem(BaseModel):
    """Single item in bulk update"""
    item_id: UUID
    is_available: Optional[bool] = None
    price: Optional[Decimal] = None


class BulkUpdateMenuRequest(BaseModel):
    """Request to bulk update menu items"""
    items: List[BulkUpdateMenuItem] = Field(..., min_items=1, max_items=100)


class BulkUpdateMenuResponse(BaseModel):
    """Response for bulk update"""
    updated_count: int
    failed_count: int
    errors: Optional[List[str]] = []


# ============================================================================
# RESTAURANT PROFILE SCHEMAS
# ============================================================================

class RestaurantProfileResponse(BaseModel):
    """Restaurant profile response"""
    restaurant_id: UUID
    name: str
    description: Optional[str] = None
    phone: str
    email: Optional[str] = None
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: str
    latitude: Decimal
    longitude: Decimal
    cuisine_type: str
    avg_delivery_time: Optional[int] = None
    min_order_amount: Optional[Decimal] = None
    delivery_fee: Optional[Decimal] = None
    platform_fee: Optional[Decimal] = None
    rating: Optional[Decimal] = None
    total_ratings: Optional[int] = 0
    is_open: bool = True
    is_veg: bool = False
    is_pure_veg: bool = False
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    image: Optional[str] = None
    cover_image: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UpdateRestaurantProfileRequest(BaseModel):
    """Request to update restaurant profile"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    cuisine_type: Optional[str] = Field(None, max_length=100)
    avg_delivery_time: Optional[int] = Field(None, ge=0)
    min_order_amount: Optional[float] = Field(None, ge=0)
    delivery_fee: Optional[float] = Field(None, ge=0)
    is_open: Optional[bool] = None
    opening_time: Optional[str] = None  # Format: "HH:MM"
    closing_time: Optional[str] = None  # Format: "HH:MM"
    image: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)


class UpdateOperatingHoursRequest(BaseModel):
    """Request to update operating hours"""
    opening_time: str = Field(..., description="Format: HH:MM (24-hour)")
    closing_time: str = Field(..., description="Format: HH:MM (24-hour)")
    is_open: bool = True
    
    @validator('opening_time', 'closing_time')
    def validate_time_format(cls, v):
        import re
        if not re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', v):
            raise ValueError('Time must be in HH:MM format (24-hour)')
        return v


# ============================================================================
# CATEGORY SCHEMAS
# ============================================================================

class CategoryResponse(BaseModel):
    """Category response"""
    category_id: UUID
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0
    
    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    """List of categories"""
    categories: List[CategoryResponse]
    total_count: int
