from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, time
from decimal import Decimal
from uuid import UUID
from app.utils.enums import RestaurantStatus


# Request Schemas
class NearbyRestaurantsRequest(BaseModel):
    """Request schema for getting nearby restaurants"""
    latitude: float = Field(..., ge=-90, le=90, description="User's latitude")
    longitude: float = Field(..., ge=-180, le=180, description="User's longitude")
    radius_km: Optional[float] = Field(5.0, ge=0.1, le=50, description="Search radius in kilometers")
    limit: Optional[int] = Field(10, ge=1, le=100, description="Number of restaurants to return")
    offset: Optional[int] = Field(0, ge=0, description="Pagination offset")
    is_veg_only: Optional[bool] = Field(None, description="Filter for pure vegetarian restaurants")
    is_open: Optional[bool] = Field(None, description="Filter for currently open restaurants")
    sort_by: Optional[str] = Field("distance", description="Sort by: distance, rating, delivery_time")
    
    @validator('sort_by')
    def validate_sort_by(cls, v):
        valid_sorts = ['distance', 'rating', 'delivery_time', 'cost_low', 'cost_high']
        if v not in valid_sorts:
            raise ValueError(f'sort_by must be one of: {", ".join(valid_sorts)}')
        return v


class RestaurantDetailRequest(BaseModel):
    """Request schema for getting restaurant details"""
    include_menu: Optional[bool] = Field(False, description="Include menu items")
    include_reviews: Optional[bool] = Field(False, description="Include reviews")
    include_offers: Optional[bool] = Field(True, description="Include active offers")


class RestaurantMenuRequest(BaseModel):
    """Request schema for getting restaurant menu"""
    category_id: Optional[UUID] = Field(None, description="Filter by category")
    is_veg: Optional[bool] = Field(None, description="Filter vegetarian items")
    is_available: Optional[bool] = Field(True, description="Only show available items")
    search: Optional[str] = Field(None, max_length=100, description="Search in item names")


class SearchRestaurantsRequest(BaseModel):
    """Request schema for searching restaurants"""
    query: Optional[str] = Field(None, max_length=100, description="Search term")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: Optional[float] = Field(5.0, ge=0.1, le=50)
    cuisine_type: Optional[str] = Field(None, description="Filter by cuisine (comma-separated)")
    is_pure_veg: Optional[bool] = None
    is_open: Optional[bool] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    max_delivery_time: Optional[int] = Field(None, ge=0)
    has_offers: Optional[bool] = None
    sort_by: Optional[str] = Field("distance")
    limit: Optional[int] = Field(10, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0)


# Response Schemas
class RestaurantOfferResponse(BaseModel):
    """Response schema for restaurant offers"""
    offer_id: UUID
    title: str
    description: Optional[str]
    discount_type: str
    discount_value: Decimal
    min_order_amount: Optional[Decimal]
    max_discount_amount: Optional[Decimal]
    valid_from: datetime
    valid_until: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class RestaurantLocationResponse(BaseModel):
    """Response schema for restaurant location"""
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    postal_code: str
    latitude: Decimal
    longitude: Decimal
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class RestaurantBasicResponse(BaseModel):
    """Basic restaurant information response"""
    restaurant_id: UUID
    name: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    image: Optional[str] = None
    cover_image: Optional[str] = None
    rating: Decimal = Decimal('0.0')
    total_ratings: int = 0
    avg_delivery_time: Optional[int] = None
    delivery_fee: Optional[Decimal] = None
    min_order_amount: Optional[Decimal] = None
    cost_for_two: Optional[Decimal] = None
    platform_fee: Optional[Decimal] = None
    status: str = 'active'
    is_open: bool = False
    is_veg: bool = False
    is_pure_veg: bool = False
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    distance: Optional[float] = Field(None, description="Distance in kilometers")
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v),
            time: lambda v: v.strftime('%H:%M:%S') if v else None
        }


class RestaurantResponse(RestaurantBasicResponse):
    """Complete restaurant response with nested data"""
    location: RestaurantLocationResponse
    offers: List[RestaurantOfferResponse] = []
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v),
            time: lambda v: v.strftime('%H:%M:%S') if v else None
        }


class NearbyRestaurantsResponse(BaseModel):
    """Response schema for nearby restaurants list"""
    restaurants: List[RestaurantResponse]
    total_count: int
    has_more: bool
    
    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    """Response schema for food category"""
    category_id: UUID
    name: str
    description: Optional[str]
    image: Optional[str]
    is_active: bool
    sort_order: int
    
    class Config:
        from_attributes = True


class FoodItemBasicResponse(BaseModel):
    """Basic food item response"""
    food_item_id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    discount_price: Optional[Decimal]
    image: Optional[str]
    is_veg: bool
    is_popular: bool
    is_recommended: bool
    rating: Decimal
    total_ratings: int
    prep_time: Optional[int]
    calories: Optional[int]
    category: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class PopularDishResponse(BaseModel):
    """Response schema for popular dish with restaurant info"""
    food_item_id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    discount_price: Optional[Decimal]
    image: Optional[str]
    is_veg: bool
    is_popular: bool
    is_recommended: bool
    rating: Decimal
    total_ratings: int
    prep_time: Optional[int]
    calories: Optional[int]
    category: Optional[str] = None
    restaurant: RestaurantBasicResponse
    distance: Optional[float] = Field(None, description="Distance in kilometers")
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class PopularDishesResponse(BaseModel):
    """Response schema for popular dishes list"""
    dishes: List[PopularDishResponse]
    total_count: int
    has_more: bool
    
    class Config:
        from_attributes = True


class CategoriesResponse(BaseModel):
    """Response schema for categories list"""
    categories: List[CategoryResponse]
    total_count: int
    
    class Config:
        from_attributes = True


class MenuItemResponse(BaseModel):
    """Response schema for menu item"""
    food_item_id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    discount_price: Optional[Decimal]
    image: Optional[str]
    is_veg: bool
    ingredients: Optional[str]
    allergens: Optional[str]
    calories: Optional[int]
    prep_time: Optional[int]
    status: str
    rating: Decimal
    total_ratings: int
    is_popular: bool
    is_recommended: bool
    nutrition_info: Optional[dict] = None
    preparation_time: Optional[str]
    category: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class MenuCategoryResponse(BaseModel):
    """Response schema for menu category with items"""
    category_id: UUID
    name: str
    description: Optional[str]
    image: Optional[str]
    is_active: bool
    sort_order: int
    items: List[MenuItemResponse] = []
    
    class Config:
        from_attributes = True


class RestaurantMenuResponse(BaseModel):
    """Response schema for restaurant menu"""
    categories: List[MenuCategoryResponse]
    total_items: int
    
    class Config:
        from_attributes = True


class RestaurantDetailResponse(RestaurantResponse):
    """Detailed restaurant response with contact info and menu"""
    phone: str
    email: Optional[str]
    created_at: datetime
    updated_at: datetime
    menu: Optional[RestaurantMenuResponse] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v),
            time: lambda v: v.strftime('%H:%M:%S') if v else None
        }

        # [NEW] Admin Response Schemas
class AdminRestaurantListItem(BaseModel):
    """Schema for individual restaurant item in admin list"""
    restaurant_id: UUID
    name: str
    image: Optional[str]
    status: str
    owner_name: str
    owner_id: UUID
    is_veg: bool
    city: str
    area: str
    created_at: datetime

    class Config:
        from_attributes = True

class AdminRestaurantListResponse(BaseModel):
    """Schema for admin restaurant list response with pagination"""
    items: List[AdminRestaurantListItem]
    total_count: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True


