import traceback
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.orm import Session
from app.infra.db.postgres.postgres_config import get_db
from app.api.schemas.common_schemas import CommonResponse
from app.api.schemas.home_schema import (
    BannerListResponse, FoodCategoryListResponse, NearbyRestaurantsResponse,
    PopularDishesResponse, AvailableCouponsResponse, HomePageDataResponse,
    LocationRequest, PopularDishesRequest, NearbyRestaurantsRequest
)
from app.domain.services.home_service import HomeService
from app.config.logger import get_logger

router = APIRouter()

@router.get("/home/banners", 
           response_model=CommonResponse[BannerListResponse],
           status_code=status.HTTP_200_OK,
           tags=["Home"])
async def get_promotional_banners(
    db: Session = Depends(get_db),
):
    """
    Get promotional banners and carousel items for home page.
    
    Returns a list of active promotional banners with gradient colors,
    icons, and offer details for the home page carousel.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing GET /home/banners request")
        
        home_service = HomeService(db)
        banners = home_service.get_promotional_banners()
        
        logger.info(f"Successfully retrieved {banners.total_count} banners")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Banners retrieved successfully",
            message_id="0",
            data=banners
        )
        
    except Exception as e:
        logger.error(f"Error in get_promotional_banners: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve banners"
        )

@router.get("/home/categories", 
           response_model=CommonResponse[FoodCategoryListResponse],
           status_code=status.HTTP_200_OK,
           tags=["Home"])
async def get_food_categories(
    db: Session = Depends(get_db),
):
    """
    Get food categories for home page.
    
    Returns a list of food categories with icons, colors, and item counts
    for browsing different types of cuisine.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing GET /home/categories request")
        
        home_service = HomeService(db)
        categories = home_service.get_food_categories()
        
        logger.info(f"Successfully retrieved {categories.total_count} categories")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Categories retrieved successfully",
            message_id="0",
            data=categories
        )
        
    except Exception as e:
        logger.error(f"Error in get_food_categories: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve categories"
        )

@router.post("/home/nearby-restaurants", 
            response_model=CommonResponse[NearbyRestaurantsResponse],
            status_code=status.HTTP_200_OK,
            tags=["Home"])
async def get_nearby_restaurants(
    request: NearbyRestaurantsRequest,
    db: Session = Depends(get_db),
):
    """
    Get nearby restaurants based on user location.
    
    Returns a list of restaurants near the user's location with filtering
    options for cuisine type, rating, delivery time, and availability.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing POST /home/nearby-restaurants request for location: "
                   f"({request.location.latitude}, {request.location.longitude})")
        
        home_service = HomeService(db)
        restaurants = home_service.get_nearby_restaurants(request)
        
        logger.info(f"Successfully retrieved {restaurants.total_count} nearby restaurants")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Nearby restaurants retrieved successfully",
            message_id="0",
            data=restaurants
        )
        
    except Exception as e:
        logger.error(f"Error in get_nearby_restaurants: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve nearby restaurants"
        )

@router.post("/home/popular-dishes", 
            response_model=CommonResponse[PopularDishesResponse],
            status_code=status.HTTP_200_OK,
            tags=["Home"])
async def get_popular_dishes(
    request: PopularDishesRequest,
    db: Session = Depends(get_db),
):
    """
    Get popular dishes with filtering options.
    
    Returns a list of popular and trending dishes with filters for
    category, vegetarian preference, price range, and location.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing POST /home/popular-dishes request")
        
        home_service = HomeService(db)
        dishes = home_service.get_popular_dishes(request)
        
        logger.info(f"Successfully retrieved {dishes.total_count} popular dishes")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Popular dishes retrieved successfully",
            message_id="0",
            data=dishes
        )
        
    except Exception as e:
        logger.error(f"Error in get_popular_dishes: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve popular dishes"
        )

@router.get("/home/coupons", 
           response_model=CommonResponse[AvailableCouponsResponse],
           status_code=status.HTTP_200_OK,
           tags=["Home"])
async def get_available_coupons(
    db: Session = Depends(get_db),
):
    """
    Get available coupons and offers.
    
    Returns a list of active coupons and promotional offers
    that users can apply to their orders.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing GET /home/coupons request")
        
        home_service = HomeService(db)
        coupons = home_service.get_available_coupons()
        
        logger.info(f"Successfully retrieved {coupons.total_count} available coupons")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Available coupons retrieved successfully",
            message_id="0",
            data=coupons
        )
        
    except Exception as e:
        logger.error(f"Error in get_available_coupons: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve available coupons"
        )

@router.post("/home/data", 
            response_model=CommonResponse[HomePageDataResponse],
            status_code=status.HTTP_200_OK,
            tags=["Home"])
async def get_home_page_data(
    location: Optional[LocationRequest] = Body(None),
    db: Session = Depends(get_db),
):
    """
    Get aggregated home page data.
    
    Returns all data needed for the home page including banners, categories,
    nearby restaurants (if location provided), popular dishes, and available coupons.
    This is an optimized endpoint to reduce multiple API calls from the frontend.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing POST /home/data request")
        if location:
            logger.info(f"Location provided: ({location.latitude}, {location.longitude})")
        
        home_service = HomeService(db)
        home_data = home_service.get_home_page_data(location)
        
        logger.info("Successfully retrieved aggregated home page data")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Home page data retrieved successfully",
            message_id="0",
            data=home_data
        )
        
    except Exception as e:
        logger.error(f"Error in get_home_page_data: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve home page data"
        )

# Additional utility endpoints for home page

@router.get("/home/categories/{category_id}/items", 
           response_model=CommonResponse[PopularDishesResponse],
           status_code=status.HTTP_200_OK,
           tags=["Home"])
async def get_items_by_category(
    category_id: str,
    location_lat: Optional[float] = Query(None, description="User's latitude"),
    location_lng: Optional[float] = Query(None, description="User's longitude"),
    is_veg: Optional[bool] = Query(None, description="Filter vegetarian items"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    limit: Optional[int] = Query(20, ge=1, le=100, description="Number of items to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of items to skip"),
    db: Session = Depends(get_db),
):
    """
    Get food items by category.
    
    Returns food items filtered by category with optional location,
    vegetarian, and price filters.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing GET /home/categories/{category_id}/items request")
        
        # Build location request if coordinates provided
        location = None
        if location_lat is not None and location_lng is not None:
            location = LocationRequest(latitude=location_lat, longitude=location_lng)
        
        # Build request object
        request = PopularDishesRequest(
            location=location,
            category=category_id,  # Using category_id as category name for now
            is_veg=is_veg,
            max_price=max_price,
            limit=limit,
            offset=offset
        )
        
        home_service = HomeService(db)
        dishes = home_service.get_popular_dishes(request)
        
        logger.info(f"Successfully retrieved {dishes.total_count} items for category {category_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message=f"Items for category {category_id} retrieved successfully",
            message_id="0",
            data=dishes
        )
        
    except Exception as e:
        logger.error(f"Error in get_items_by_category: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve items by category"
        ) 