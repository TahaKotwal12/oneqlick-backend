import traceback
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from app.infra.db.postgres.postgres_config import get_db
from app.api.schemas.common_schemas import CommonResponse
from app.api.schemas.restaurant_schema import (
    RestaurantCreateRequest, RestaurantUpdateRequest, RestaurantResponse, 
    RestaurantListResponse, RestaurantStatus
)
from app.domain.services.restaurant_service import RestaurantService
from app.config.logger import get_logger

router = APIRouter()

@router.post("/restaurants", 
            response_model=CommonResponse[RestaurantResponse],
            status_code=status.HTTP_201_CREATED,
            tags=["Restaurants"])
async def create_restaurant(
    restaurant_data: RestaurantCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Create a new restaurant in the OneQlick food delivery system.
    
    This endpoint creates a new restaurant with the provided information.
    Phone number must be unique across the system.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing POST /restaurants request for restaurant: {restaurant_data.name}")
        
        restaurant_service = RestaurantService(db)
        restaurant = restaurant_service.create_restaurant(restaurant_data)
        
        logger.info(f"Successfully created restaurant with ID: {restaurant.restaurant_id}")
        return CommonResponse(
            code=status.HTTP_201_CREATED,
            message="Restaurant created successfully",
            message_id="0",
            data=RestaurantResponse.model_validate(restaurant)
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in create_restaurant: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Error in create_restaurant: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the restaurant"
        )

@router.get("/restaurants/{restaurant_id}", 
            response_model=CommonResponse[RestaurantResponse],
            tags=["Restaurants"])
async def get_restaurant_by_id(
    restaurant_id: UUID = Path(..., description="The UUID of the restaurant to fetch"),
    db: Session = Depends(get_db),
):
    """
    Get restaurant details by UUID.
    
    This endpoint retrieves a restaurant's complete information from the OneQlick food delivery system.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing GET /restaurants/{restaurant_id} request")
        
        restaurant_service = RestaurantService(db)
        restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        logger.info(f"Successfully retrieved restaurant data for UUID {restaurant_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Restaurant details retrieved successfully",
            message_id="0",
            data=RestaurantResponse.model_validate(restaurant)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in get_restaurant_by_id: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching restaurant details"
        )

@router.get("/restaurants", 
            response_model=CommonResponse[List[RestaurantListResponse]],
            tags=["Restaurants"])
async def get_all_restaurants(
    skip: int = Query(0, ge=0, description="Number of restaurants to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of restaurants to return"),
    status_filter: Optional[RestaurantStatus] = Query(None, alias="status", description="Filter by restaurant status"),
    cuisine_type: Optional[str] = Query(None, description="Filter by cuisine type"),
    city: Optional[str] = Query(None, description="Filter by city"),
    is_open: Optional[bool] = Query(None, description="Filter by open/closed status"),
    db: Session = Depends(get_db),
):
    """
    Get all restaurants with optional filtering.
    
    This endpoint retrieves a list of restaurants with pagination and optional filtering by status, cuisine type, city, and open status.
    Returns empty list if no restaurants match the criteria.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing GET /restaurants request with skip={skip}, limit={limit}, status={status_filter}, cuisine_type={cuisine_type}, city={city}, is_open={is_open}")
        
        restaurant_service = RestaurantService(db)
        restaurants = restaurant_service.get_all_restaurants(
            skip=skip, 
            limit=limit, 
            status=status_filter.value if status_filter else None,
            cuisine_type=cuisine_type,
            city=city,
            is_open=is_open
        )
        
        message = f"Retrieved {len(restaurants)} restaurants successfully"
        if len(restaurants) == 0:
            message = "No restaurants found matching the criteria"
        
        logger.info(f"Successfully retrieved {len(restaurants)} restaurants")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message=message,
            message_id="0",
            data=[RestaurantListResponse.model_validate(restaurant) for restaurant in restaurants]
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in get_all_restaurants: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Error in get_all_restaurants: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching restaurants"
        )

@router.get("/restaurants/owner/{owner_id}", 
            response_model=CommonResponse[List[RestaurantListResponse]],
            tags=["Restaurants"])
async def get_restaurants_by_owner(
    owner_id: UUID = Path(..., description="The UUID of the restaurant owner"),
    db: Session = Depends(get_db),
):
    """
    Get all restaurants owned by a specific user.
    
    This endpoint retrieves all restaurants owned by the specified user.
    Returns empty list if owner not found or has no restaurants.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing GET /restaurants/owner/{owner_id} request")
        
        restaurant_service = RestaurantService(db)
        restaurants = restaurant_service.get_restaurants_by_owner(owner_id)
        
        message = f"Retrieved {len(restaurants)} restaurants for owner successfully"
        if len(restaurants) == 0:
            message = "No restaurants found for this owner"
        
        logger.info(f"Successfully retrieved {len(restaurants)} restaurants for owner {owner_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message=message,
            message_id="0",
            data=[RestaurantListResponse.model_validate(restaurant) for restaurant in restaurants]
        )
        
    except Exception as e:
        error_msg = f"Error in get_restaurants_by_owner: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching owner's restaurants"
        )

@router.get("/restaurants/search/location", 
            response_model=CommonResponse[List[RestaurantListResponse]],
            tags=["Restaurants"])
async def search_restaurants_by_location(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude coordinate"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude coordinate"),
    radius_km: float = Query(10.0, ge=0.1, le=100.0, description="Search radius in kilometers"),
    db: Session = Depends(get_db),
):
    """
    Search restaurants by location.
    
    This endpoint searches for restaurants within a specified radius of given coordinates.
    Returns empty list if no restaurants found in the specified area.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing GET /restaurants/search/location request with lat={latitude}, lon={longitude}, radius={radius_km}km")
        
        restaurant_service = RestaurantService(db)
        restaurants = restaurant_service.search_restaurants_by_location(latitude, longitude, radius_km)
        
        message = f"Found {len(restaurants)} restaurants within {radius_km}km"
        if len(restaurants) == 0:
            message = f"No restaurants found within {radius_km}km of the specified location"
        
        logger.info(f"Successfully found {len(restaurants)} restaurants within {radius_km}km")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message=message,
            message_id="0",
            data=[RestaurantListResponse.model_validate(restaurant) for restaurant in restaurants]
        )
        
    except Exception as e:
        error_msg = f"Error in search_restaurants_by_location: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching restaurants by location"
        )

@router.put("/restaurants/{restaurant_id}", 
            response_model=CommonResponse[RestaurantResponse],
            tags=["Restaurants"])
async def update_restaurant(
    restaurant_id: UUID = Path(..., description="The UUID of the restaurant to update"),
    update_data: RestaurantUpdateRequest = ...,
    db: Session = Depends(get_db),
):
    """
    Update restaurant information.
    
    This endpoint updates an existing restaurant's information. Only provided fields will be updated.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing PUT /restaurants/{restaurant_id} request")
        
        restaurant_service = RestaurantService(db)
        restaurant = restaurant_service.update_restaurant(restaurant_id, update_data)
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        logger.info(f"Successfully updated restaurant {restaurant_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Restaurant updated successfully",
            message_id="0",
            data=RestaurantResponse.model_validate(restaurant)
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in update_restaurant: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in update_restaurant: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the restaurant"
        )

@router.delete("/restaurants/{restaurant_id}", 
               response_model=CommonResponse[dict],
               tags=["Restaurants"])
async def delete_restaurant(
    restaurant_id: UUID = Path(..., description="The UUID of the restaurant to delete"),
    db: Session = Depends(get_db),
):
    """
    Delete a restaurant (soft delete).
    
    This endpoint performs a soft delete by setting the restaurant status to inactive.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing DELETE /restaurants/{restaurant_id} request")
        
        restaurant_service = RestaurantService(db)
        result = restaurant_service.delete_restaurant(restaurant_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        logger.info(f"Successfully deleted restaurant {restaurant_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Restaurant deleted successfully",
            message_id="0",
            data={"restaurant_id": str(restaurant_id), "deleted": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in delete_restaurant: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the restaurant"
        )

@router.post("/restaurants/{restaurant_id}/toggle-status", 
             response_model=CommonResponse[dict],
             tags=["Restaurants"])
async def toggle_restaurant_status(
    restaurant_id: UUID = Path(..., description="The UUID of the restaurant to toggle status"),
    db: Session = Depends(get_db),
):
    """
    Toggle restaurant open/closed status.
    
    This endpoint toggles the restaurant's open/closed status.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing POST /restaurants/{restaurant_id}/toggle-status request")
        
        restaurant_service = RestaurantService(db)
        result = restaurant_service.toggle_restaurant_status(restaurant_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        logger.info(f"Successfully toggled status for restaurant {restaurant_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Restaurant status toggled successfully",
            message_id="0",
            data={"restaurant_id": str(restaurant_id), "status_toggled": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in toggle_restaurant_status: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while toggling restaurant status"
        )

@router.post("/restaurants/{restaurant_id}/rate", 
             response_model=CommonResponse[dict],
             tags=["Restaurants"])
async def rate_restaurant(
    restaurant_id: UUID = Path(..., description="The UUID of the restaurant to rate"),
    rating: float = Query(..., ge=1, le=5, description="Rating value between 1 and 5"),
    db: Session = Depends(get_db),
):
    """
    Rate a restaurant.
    
    This endpoint adds a rating to the restaurant and updates the average rating.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing POST /restaurants/{restaurant_id}/rate request with rating={rating}")
        
        restaurant_service = RestaurantService(db)
        result = restaurant_service.update_restaurant_rating(restaurant_id, rating)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        logger.info(f"Successfully rated restaurant {restaurant_id} with rating {rating}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Restaurant rated successfully",
            message_id="0",
            data={"restaurant_id": str(restaurant_id), "rating": rating, "rated": True}
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in rate_restaurant: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in rate_restaurant: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while rating the restaurant"
        )

@router.get("/restaurants/{restaurant_id}/statistics", 
            response_model=CommonResponse[dict],
            tags=["Restaurants"])
async def get_restaurant_statistics(
    restaurant_id: UUID = Path(..., description="The UUID of the restaurant to get statistics for"),
    db: Session = Depends(get_db),
):
    """
    Get restaurant statistics.
    
    This endpoint retrieves statistics for a specific restaurant.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing GET /restaurants/{restaurant_id}/statistics request")
        
        restaurant_service = RestaurantService(db)
        stats = restaurant_service.get_restaurant_statistics(restaurant_id)
        
        logger.info(f"Successfully retrieved statistics for restaurant {restaurant_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Restaurant statistics retrieved successfully",
            message_id="0",
            data=stats
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in get_restaurant_statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Error in get_restaurant_statistics: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving restaurant statistics"
        ) 