from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from uuid import UUID

# ====================================================================
# BANNER/CAROUSEL SCHEMAS
# ====================================================================

class BannerResponse(BaseModel):
    """Response schema for promotional banners/carousel items"""
    id: str
    title: str
    subtitle: str
    description: str
    icon: str
    gradient_colors: List[str]
    action_text: str
    badge: Optional[str] = None
    offer_code: Optional[str] = None
    discount: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0

class BannerListResponse(BaseModel):
    """Response schema for list of banners"""
    banners: List[BannerResponse]
    total_count: int

# ====================================================================
# FOOD CATEGORY SCHEMAS
# ====================================================================

class FoodCategoryResponse(BaseModel):
    """Response schema for food categories"""
    id: str
    name: str
    icon: str
    color: str
    item_count: int
    is_active: bool = True
    sort_order: int = 0

class FoodCategoryListResponse(BaseModel):
    """Response schema for list of food categories"""
    categories: List[FoodCategoryResponse]
    total_count: int

# ====================================================================
# RESTAURANT SCHEMAS
# ====================================================================

class RestaurantSummaryResponse(BaseModel):
    """Summary response schema for restaurants (for home page listing)"""
    id: str
    name: str
    cuisine: str
    rating: float
    delivery_time: str
    min_order: str
    distance: str
    image: str
    is_open: bool
    offers: List[str]

class NearbyRestaurantsResponse(BaseModel):
    """Response schema for nearby restaurants"""
    restaurants: List[RestaurantSummaryResponse]
    total_count: int
    user_location: Optional[dict] = None

# ====================================================================
# FOOD ITEM/DISH SCHEMAS
# ====================================================================

class FoodItemResponse(BaseModel):
    """Response schema for food items/dishes"""
    id: str
    name: str
    description: str
    price: Decimal
    image: str
    category: str
    is_veg: bool
    is_available: bool = True
    is_popular: bool = False
    is_recommended: bool = False
    restaurant_id: Optional[str] = None
    restaurant_name: Optional[str] = None
    rating: Optional[float] = None
    prep_time: Optional[int] = None

class PopularDishesResponse(BaseModel):
    """Response schema for popular dishes"""
    dishes: List[FoodItemResponse]
    total_count: int
    filters: List[str] = ["All", "Veg", "Non-Veg", "Under ₹200", "Quick Bites"]

# ====================================================================
# COUPON/OFFER SCHEMAS
# ====================================================================

class CouponResponse(BaseModel):
    """Response schema for coupons and offers"""
    id: str
    code: str
    title: str
    description: str
    coupon_type: str  # 'percentage', 'fixed_amount', 'free_delivery'
    discount_value: Decimal
    min_order_amount: Decimal
    max_discount_amount: Optional[Decimal] = None
    valid_until: str
    is_active: bool = True
    terms_conditions: Optional[str] = None

class AvailableCouponsResponse(BaseModel):
    """Response schema for available coupons"""
    coupons: List[CouponResponse]
    total_count: int

# ====================================================================
# HOME PAGE AGGREGATE SCHEMAS
# ====================================================================

class HomePageDataResponse(BaseModel):
    """Aggregate response schema for all home page data"""
    banners: List[BannerResponse]
    categories: List[FoodCategoryResponse]
    nearby_restaurants: List[RestaurantSummaryResponse]
    popular_dishes: List[FoodItemResponse]
    available_coupons: List[CouponResponse]
    user_location: Optional[dict] = None

# ====================================================================
# REQUEST SCHEMAS
# ====================================================================

class LocationRequest(BaseModel):
    """Request schema for location-based queries"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius: Optional[float] = Field(5.0, ge=0.1, le=50)  # in kilometers

class PopularDishesRequest(BaseModel):
    """Request schema for popular dishes with filters"""
    location: Optional[LocationRequest] = None
    category: Optional[str] = None
    is_veg: Optional[bool] = None
    max_price: Optional[Decimal] = None
    limit: Optional[int] = Field(20, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0)

class NearbyRestaurantsRequest(BaseModel):
    """Request schema for nearby restaurants"""
    location: LocationRequest
    cuisine: Optional[str] = None
    is_open: Optional[bool] = True
    min_rating: Optional[float] = None
    max_delivery_time: Optional[int] = None
    limit: Optional[int] = Field(20, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0) 