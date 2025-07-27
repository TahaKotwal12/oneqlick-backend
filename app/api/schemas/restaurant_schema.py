from pydantic import BaseModel, Field, EmailStr, validator
from uuid import UUID
from typing import Optional
from datetime import datetime, time
from enum import Enum
from decimal import Decimal

class RestaurantStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'
    suspended = 'suspended'

class RestaurantCreateRequest(BaseModel):
    owner_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    phone: str = Field(..., min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    latitude: Decimal = Field(..., ge=-90, le=90)
    longitude: Decimal = Field(..., ge=-180, le=180)
    image: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)
    cuisine_type: Optional[str] = Field(None, max_length=100)
    avg_delivery_time: Optional[int] = Field(None, ge=0)
    min_order_amount: Optional[Decimal] = Field(0, ge=0)
    delivery_fee: Optional[Decimal] = Field(0, ge=0)
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

    @validator('avg_delivery_time')
    def validate_avg_delivery_time(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Average delivery time must be positive')
        return v

class RestaurantUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    address_line1: Optional[str] = Field(None, min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    image: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)
    cuisine_type: Optional[str] = Field(None, max_length=100)
    avg_delivery_time: Optional[int] = Field(None, ge=0)
    min_order_amount: Optional[Decimal] = Field(None, ge=0)
    delivery_fee: Optional[Decimal] = Field(None, ge=0)
    status: Optional[RestaurantStatus] = None
    is_open: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

class RestaurantResponse(BaseModel):
    restaurant_id: UUID
    owner_id: UUID
    name: str
    description: Optional[str] = None
    phone: str
    email: Optional[str] = None
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    latitude: Decimal
    longitude: Decimal
    image: Optional[str] = None
    cover_image: Optional[str] = None
    cuisine_type: Optional[str] = None
    avg_delivery_time: Optional[int] = None
    min_order_amount: Decimal
    delivery_fee: Decimal
    rating: Decimal
    total_ratings: int
    status: RestaurantStatus
    is_open: bool
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RestaurantListResponse(BaseModel):
    restaurant_id: UUID
    name: str
    description: Optional[str] = None
    phone: str
    city: str
    state: str
    cuisine_type: Optional[str] = None
    rating: Decimal
    total_ratings: int
    status: RestaurantStatus
    is_open: bool
    min_order_amount: Decimal
    delivery_fee: Decimal
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True 