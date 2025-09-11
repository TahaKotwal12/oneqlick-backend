import math
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text, func
from datetime import datetime, timedelta
from decimal import Decimal

from app.api.schemas.home_schema import (
    BannerResponse, BannerListResponse,
    FoodCategoryResponse, FoodCategoryListResponse,
    RestaurantSummaryResponse, NearbyRestaurantsResponse,
    FoodItemResponse, PopularDishesResponse,
    CouponResponse, AvailableCouponsResponse,
    HomePageDataResponse,
    LocationRequest, PopularDishesRequest, NearbyRestaurantsRequest
)

class HomeService:
    """Service class for home page related operations"""
    
    def __init__(self, db: Session):
        self.db = db

    def get_promotional_banners(self) -> BannerListResponse:
        """
        Get promotional banners/carousel items for home page
        Currently returns mock data - will be replaced with database queries
        """
        # Mock data matching frontend carousel structure
        mock_banners = [
            {
                "id": "1",
                "title": "MEGA SALE",
                "subtitle": "Up to 60% OFF",
                "description": "On your first 3 orders above ₹199",
                "icon": "fire",
                "gradient_colors": ["#FF6B35", "#FF8562", "#FFA726"],
                "action_text": "Order Now",
                "badge": "LIMITED TIME",
                "offer_code": "MEGA60",
                "discount": "60%",
                "is_active": True,
                "sort_order": 1
            },
            {
                "id": "2",
                "title": "FREE DELIVERY",
                "subtitle": "No delivery charges",
                "description": "On orders above ₹299 from top restaurants",
                "icon": "truck-delivery",
                "gradient_colors": ["#4CAF50", "#66BB6A", "#81C784"],
                "action_text": "Browse Restaurants",
                "badge": "POPULAR",
                "offer_code": "FREEDEL",
                "discount": None,
                "is_active": True,
                "sort_order": 2
            },
            {
                "id": "3",
                "title": "FLAT ₹100 OFF",
                "subtitle": "Weekend Special",
                "description": "Valid on minimum order of ₹500",
                "icon": "percent",
                "gradient_colors": ["#2196F3", "#42A5F5", "#64B5F6"],
                "action_text": "Grab Deal",
                "badge": "WEEKEND",
                "offer_code": "WEEK100",
                "discount": "₹100",
                "is_active": True,
                "sort_order": 3
            },
            {
                "id": "4",
                "title": "CASHBACK ₹50",
                "subtitle": "Pay with UPI",
                "description": "Get instant cashback on UPI payments",
                "icon": "wallet",
                "gradient_colors": ["#9C27B0", "#BA68C8", "#CE93D8"],
                "action_text": "Pay Now",
                "badge": "INSTANT",
                "offer_code": "UPI50",
                "discount": "₹50",
                "is_active": True,
                "sort_order": 4
            },
            {
                "id": "5",
                "title": "COMBO DEALS",
                "subtitle": "Buy 1 Get 1 FREE",
                "description": "On selected items from partner restaurants",
                "icon": "food-variant",
                "gradient_colors": ["#FF5722", "#FF7043", "#FF8A65"],
                "action_text": "View Combos",
                "badge": "HOT DEAL",
                "offer_code": None,
                "discount": None,
                "is_active": True,
                "sort_order": 5
            }
        ]
        
        banners = [BannerResponse(**banner) for banner in mock_banners]
        return BannerListResponse(banners=banners, total_count=len(banners))

    def get_food_categories(self) -> FoodCategoryListResponse:
        """
        Get food categories for home page
        Currently returns mock data - will be replaced with database queries
        """
        mock_categories = [
            {"id": "1", "name": "Biryani", "icon": "food-variant", "color": "#FF6B35", "item_count": 45, "is_active": True, "sort_order": 1},
            {"id": "2", "name": "Pizza", "icon": "pizza", "color": "#FFD93D", "item_count": 32, "is_active": True, "sort_order": 2},
            {"id": "3", "name": "Chinese", "icon": "noodles", "color": "#6BCF7F", "item_count": 28, "is_active": True, "sort_order": 3},
            {"id": "4", "name": "South Indian", "icon": "food-drumstick", "color": "#4ECDC4", "item_count": 38, "is_active": True, "sort_order": 4},
            {"id": "5", "name": "Sweets", "icon": "cupcake", "color": "#FF8E9E", "item_count": 25, "is_active": True, "sort_order": 5},
            {"id": "6", "name": "Tea/Coffee", "icon": "coffee", "color": "#A8E6CF", "item_count": 18, "is_active": True, "sort_order": 6},
            {"id": "7", "name": "Fast Food", "icon": "hamburger", "color": "#FFB74D", "item_count": 42, "is_active": True, "sort_order": 7},
            {"id": "8", "name": "Healthy", "icon": "food-apple", "color": "#81C784", "item_count": 55, "is_active": True, "sort_order": 8}
        ]
        
        categories = [FoodCategoryResponse(**category) for category in mock_categories]
        return FoodCategoryListResponse(categories=categories, total_count=len(categories))

    def get_nearby_restaurants(self, request: NearbyRestaurantsRequest) -> NearbyRestaurantsResponse:
        """
        Get nearby restaurants based on user location
        Currently returns mock data - will be replaced with database queries using PostGIS
        """
        # Calculate distance using Haversine formula (mock implementation)
        mock_restaurants = [
            {
                "id": "1",
                "name": "Spice Garden",
                "cuisine": "North Indian",
                "rating": 4.5,
                "delivery_time": "25-35 min",
                "min_order": "₹150",
                "distance": "0.8 km",
                "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200&fit=crop&crop=center",
                "is_open": True,
                "offers": ["20% OFF", "Free Delivery"]
            },
            {
                "id": "2",
                "name": "Pizza Palace",
                "cuisine": "Italian",
                "rating": 4.3,
                "delivery_time": "30-40 min",
                "min_order": "₹200",
                "distance": "1.2 km",
                "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop&crop=center",
                "is_open": True,
                "offers": ["Buy 1 Get 1"]
            },
            {
                "id": "3",
                "name": "Biryani House",
                "cuisine": "Hyderabadi",
                "rating": 4.7,
                "delivery_time": "20-30 min",
                "min_order": "₹180",
                "distance": "0.5 km",
                "image": "https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=300&h=200&fit=crop&crop=center",
                "is_open": True,
                "offers": ["15% OFF"]
            },
            {
                "id": "4",
                "name": "Sweet Corner",
                "cuisine": "Desserts",
                "rating": 4.2,
                "delivery_time": "15-25 min",
                "min_order": "₹100",
                "distance": "0.3 km",
                "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop&crop=center",
                "is_open": True,
                "offers": ["Diwali Special"]
            },
            {
                "id": "5",
                "name": "Chai Point",
                "cuisine": "Beverages",
                "rating": 4.0,
                "delivery_time": "10-20 min",
                "min_order": "₹50",
                "distance": "0.6 km",
                "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300&h=200&fit=crop&crop=center",
                "is_open": True,
                "offers": ["Free Tea"]
            },
            {
                "id": "6",
                "name": "Dhaba Express",
                "cuisine": "Punjabi",
                "rating": 4.4,
                "delivery_time": "35-45 min",
                "min_order": "₹120",
                "distance": "1.5 km",
                "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200&fit=crop&crop=center",
                "is_open": False,
                "offers": ["30% OFF"]
            }
        ]
        
        # Apply filters
        filtered_restaurants = mock_restaurants
        
        if request.cuisine:
            filtered_restaurants = [r for r in filtered_restaurants if request.cuisine.lower() in r["cuisine"].lower()]
        
        if request.is_open is not None:
            filtered_restaurants = [r for r in filtered_restaurants if r["is_open"] == request.is_open]
        
        if request.min_rating:
            filtered_restaurants = [r for r in filtered_restaurants if r["rating"] >= request.min_rating]
        
        # Apply pagination
        offset = request.offset or 0
        limit = request.limit or 20
        paginated_restaurants = filtered_restaurants[offset:offset + limit]
        
        restaurants = [RestaurantSummaryResponse(**restaurant) for restaurant in paginated_restaurants]
        user_location = {"latitude": request.location.latitude, "longitude": request.location.longitude}
        
        return NearbyRestaurantsResponse(
            restaurants=restaurants, 
            total_count=len(filtered_restaurants),
            user_location=user_location
        )

    def get_popular_dishes(self, request: PopularDishesRequest) -> PopularDishesResponse:
        """
        Get popular dishes with optional filters
        Currently returns mock data - will be replaced with database queries
        """
        mock_dishes = [
            {
                "id": "1",
                "name": "Butter Chicken",
                "description": "Rich and creamy butter chicken cooked in aromatic spices with tender chicken pieces",
                "price": Decimal("280"),
                "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop&crop=center",
                "category": "Main Course",
                "is_veg": False,
                "is_available": True,
                "is_popular": True,
                "is_recommended": False,
                "restaurant_id": "1",
                "restaurant_name": "Spice Garden",
                "rating": 4.5,
                "prep_time": 25
            },
            {
                "id": "2",
                "name": "Margherita Pizza",
                "description": "Classic Italian pizza with fresh tomato sauce, mozzarella cheese and basil",
                "price": Decimal("320"),
                "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=center",
                "category": "Pizza",
                "is_veg": True,
                "is_available": True,
                "is_popular": True,
                "is_recommended": False,
                "restaurant_id": "2",
                "restaurant_name": "Pizza Palace",
                "rating": 4.3,
                "prep_time": 30
            },
            {
                "id": "3",
                "name": "Hyderabadi Biryani",
                "description": "Aromatic basmati rice with tender meat, cooked with traditional spices and herbs",
                "price": Decimal("350"),
                "image": "https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=400&h=300&fit=crop&crop=center",
                "category": "Biryani",
                "is_veg": False,
                "is_available": True,
                "is_popular": True,
                "is_recommended": False,
                "restaurant_id": "3",
                "restaurant_name": "Biryani House",
                "rating": 4.7,
                "prep_time": 35
            },
            {
                "id": "4",
                "name": "Gulab Jamun",
                "description": "Sweet and soft milk solids dumplings soaked in rose-flavored sugar syrup",
                "price": Decimal("80"),
                "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=300&fit=crop&crop=center",
                "category": "Dessert",
                "is_veg": True,
                "is_available": True,
                "is_popular": True,
                "is_recommended": False,
                "restaurant_id": "4",
                "restaurant_name": "Sweet Corner",
                "rating": 4.2,
                "prep_time": 10
            },
            {
                "id": "5",
                "name": "Masala Chai",
                "description": "Spiced Indian tea with milk, ginger, cardamom and aromatic spices",
                "price": Decimal("25"),
                "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop&crop=center",
                "category": "Beverages",
                "is_veg": True,
                "is_available": True,
                "is_popular": True,
                "is_recommended": False,
                "restaurant_id": "5",
                "restaurant_name": "Chai Point",
                "rating": 4.0,
                "prep_time": 5
            },
            {
                "id": "6",
                "name": "Chicken Tikka",
                "description": "Grilled chicken tikka marinated in yogurt and spices with mint chutney",
                "price": Decimal("220"),
                "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop&crop=center",
                "category": "Appetizer",
                "is_veg": False,
                "is_available": True,
                "is_popular": True,
                "is_recommended": False,
                "restaurant_id": "1",
                "restaurant_name": "Spice Garden",
                "rating": 4.5,
                "prep_time": 20
            },
            {
                "id": "7",
                "name": "Veg Fried Rice",
                "description": "Chinese style vegetable fried rice with fresh vegetables and soy sauce",
                "price": Decimal("160"),
                "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&h=300&fit=crop&crop=center",
                "category": "Chinese",
                "is_veg": True,
                "is_available": True,
                "is_popular": True,
                "is_recommended": False,
                "restaurant_id": "3",
                "restaurant_name": "Biryani House",
                "rating": 4.1,
                "prep_time": 25
            },
            {
                "id": "8",
                "name": "Paneer Butter Masala",
                "description": "Cottage cheese cubes in rich tomato gravy with cream and butter",
                "price": Decimal("240"),
                "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop&crop=center",
                "category": "Main Course",
                "is_veg": True,
                "is_available": True,
                "is_popular": True,
                "is_recommended": False,
                "restaurant_id": "1",
                "restaurant_name": "Spice Garden",
                "rating": 4.4,
                "prep_time": 30
            }
        ]
        
        # Apply filters
        filtered_dishes = mock_dishes
        
        if request.category:
            filtered_dishes = [d for d in filtered_dishes if request.category.lower() in d["category"].lower()]
        
        if request.is_veg is not None:
            filtered_dishes = [d for d in filtered_dishes if d["is_veg"] == request.is_veg]
        
        if request.max_price:
            filtered_dishes = [d for d in filtered_dishes if d["price"] <= request.max_price]
        
        # Apply pagination
        offset = request.offset or 0
        limit = request.limit or 20
        paginated_dishes = filtered_dishes[offset:offset + limit]
        
        dishes = [FoodItemResponse(**dish) for dish in paginated_dishes]
        
        return PopularDishesResponse(
            dishes=dishes, 
            total_count=len(filtered_dishes),
            filters=["All", "Veg", "Non-Veg", "Under ₹200", "Quick Bites"]
        )

    def get_available_coupons(self) -> AvailableCouponsResponse:
        """
        Get available coupons and offers
        Currently returns mock data - will be replaced with database queries
        """
        mock_coupons = [
            {
                "id": "1",
                "code": "MEGA60",
                "title": "Mega Sale - 60% OFF",
                "description": "Get up to 60% off on your first 3 orders",
                "coupon_type": "percentage",
                "discount_value": Decimal("60"),
                "min_order_amount": Decimal("199"),
                "max_discount_amount": Decimal("200"),
                "valid_until": "2024-12-31",
                "is_active": True,
                "terms_conditions": "Valid on first 3 orders only. Maximum discount ₹200."
            },
            {
                "id": "2",
                "code": "FREEDEL",
                "title": "Free Delivery",
                "description": "Free delivery on orders above ₹299",
                "coupon_type": "free_delivery",
                "discount_value": Decimal("0"),
                "min_order_amount": Decimal("299"),
                "max_discount_amount": None,
                "valid_until": "2024-12-31",
                "is_active": True,
                "terms_conditions": "Valid on orders above ₹299 from participating restaurants."
            },
            {
                "id": "3",
                "code": "WEEK100",
                "title": "Weekend Special - ₹100 OFF",
                "description": "Flat ₹100 off on minimum order of ₹500",
                "coupon_type": "fixed_amount",
                "discount_value": Decimal("100"),
                "min_order_amount": Decimal("500"),
                "max_discount_amount": None,
                "valid_until": "2024-12-31",
                "is_active": True,
                "terms_conditions": "Valid only on weekends. One time use per user."
            },
            {
                "id": "4",
                "code": "UPI50",
                "title": "UPI Cashback - ₹50",
                "description": "Get ₹50 cashback on UPI payments",
                "coupon_type": "fixed_amount",
                "discount_value": Decimal("50"),
                "min_order_amount": Decimal("200"),
                "max_discount_amount": None,
                "valid_until": "2024-12-31",
                "is_active": True,
                "terms_conditions": "Valid only on UPI payments. Cashback credited within 24 hours."
            }
        ]
        
        coupons = [CouponResponse(**coupon) for coupon in mock_coupons]
        return AvailableCouponsResponse(coupons=coupons, total_count=len(coupons))

    def get_home_page_data(self, location: Optional[LocationRequest] = None) -> HomePageDataResponse:
        """
        Get aggregated data for home page including banners, categories, restaurants, dishes, and coupons
        """
        banners_response = self.get_promotional_banners()
        categories_response = self.get_food_categories()
        coupons_response = self.get_available_coupons()
        
        # Get popular dishes with basic request
        popular_dishes_request = PopularDishesRequest(
            location=location,
            limit=8  # Limit for home page display
        )
        popular_dishes_response = self.get_popular_dishes(popular_dishes_request)
        
        # Get nearby restaurants if location provided
        nearby_restaurants = []
        user_location = None
        if location:
            nearby_restaurants_request = NearbyRestaurantsRequest(
                location=location,
                limit=6  # Limit for home page display
            )
            nearby_response = self.get_nearby_restaurants(nearby_restaurants_request)
            nearby_restaurants = nearby_response.restaurants
            user_location = nearby_response.user_location
        
        return HomePageDataResponse(
            banners=banners_response.banners,
            categories=categories_response.categories,
            nearby_restaurants=nearby_restaurants,
            popular_dishes=popular_dishes_response.dishes,
            available_coupons=coupons_response.coupons,
            user_location=user_location
        )

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c 