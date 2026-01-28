"""
Partner Menu Management API Routes
Handles menu item CRUD operations for restaurant owners
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
import logging

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user, require_restaurant_owner
from app.api.schemas.partner_restaurant_schemas import (
    MenuItemResponse, MenuListResponse, CreateMenuItemRequest,
    UpdateMenuItemRequest, UpdateItemAvailabilityRequest,
    CategoryResponse, CategoryListResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.category import Category
from app.config.logger import get_logger

router = APIRouter(prefix="/partner/restaurant/menu", tags=["Partner - Menu"])
logger = get_logger(__name__)


# ============================================================================
# MENU ITEM MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("", response_model=CommonResponse[MenuListResponse])
async def get_menu_items(
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search by name"),
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Get all menu items for the authenticated restaurant owner.
    
    Returns menu items with category information, filtered by optional parameters.
    """
    try:
        logger.info(f"Fetching menu items for restaurant owner: {current_user.user_id}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Build query
        query = db.query(FoodItem).filter(
            FoodItem.restaurant_id == restaurant.restaurant_id
        )
        
        # Apply filters
        if category_id:
            query = query.filter(FoodItem.category_id == category_id)
        
        if search:
            query = query.filter(FoodItem.name.ilike(f"%{search}%"))
        
        # Get all items
        items = query.order_by(FoodItem.sort_order, FoodItem.name).all()
        
        # Build response with category names
        items_response = []
        for item in items:
            # Get category name
            category_name = None
            if item.category_id:
                category = db.query(Category).filter(
                    Category.category_id == item.category_id
                ).first()
                if category:
                    category_name = category.name
            
            items_response.append(MenuItemResponse(
                food_item_id=str(item.food_item_id),
                name=item.name,
                description=item.description,
                price=float(item.price),
                discount_price=float(item.discount_price) if item.discount_price else None,
                category_id=str(item.category_id) if item.category_id else None,
                category_name=category_name,
                image=item.image,
                is_veg=item.is_veg,
                is_available=(item.status == 'available'),
                ingredients=item.ingredients,
                allergens=item.allergens,
                prep_time=item.prep_time,
                calories=item.calories,
                rating=float(item.rating) if item.rating else None,
                total_ratings=item.total_ratings,
                is_popular=item.is_popular,
                is_recommended=item.is_recommended,
                created_at=item.created_at,
                updated_at=item.updated_at
            ))
        
        logger.info(f"Found {len(items_response)} menu items")
        
        return CommonResponse(
            code=200,
            message="Menu items retrieved successfully",
            message_id="MENU_ITEMS_RETRIEVED",
            data=MenuListResponse(
                items=items_response,
                total_count=len(items_response)
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching menu items: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch menu items: {str(e)}"
        )


@router.post("", response_model=CommonResponse[MenuItemResponse])
async def create_menu_item(
    request: CreateMenuItemRequest,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Create a new menu item for the restaurant.
    
    Requires restaurant owner authentication.
    """
    try:
        logger.info(f"Creating menu item for restaurant owner: {current_user.user_id}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Verify category exists
        category = db.query(Category).filter(
            Category.category_id == request.category_id
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {request.category_id} not found"
            )
        
        # Create new food item
        new_item = FoodItem(
            restaurant_id=restaurant.restaurant_id,
            category_id=request.category_id,
            name=request.name,
            description=request.description,
            price=request.price,
            image=request.image_url,
            is_veg=request.is_veg,
            ingredients=request.ingredients,
            allergens=request.allergens,
            prep_time=request.prep_time,
            calories=request.calories,
            status='available',  # Default to available
            rating=Decimal('0.00'),
            total_ratings=0,
            sort_order=0,
            is_popular=False,
            is_recommended=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        logger.info(f"Menu item created successfully: {new_item.food_item_id}")
        
        # Build response
        response_item = MenuItemResponse(
            food_item_id=str(new_item.food_item_id),
            name=new_item.name,
            description=new_item.description,
            price=float(new_item.price),
            discount_price=float(new_item.discount_price) if new_item.discount_price else None,
            category_id=str(new_item.category_id),
            category_name=category.name,
            image=new_item.image,
            is_veg=new_item.is_veg,
            is_available=True,
            ingredients=new_item.ingredients,
            allergens=new_item.allergens,
            prep_time=new_item.prep_time,
            calories=new_item.calories,
            rating=0.0,
            total_ratings=0,
            is_popular=False,
            is_recommended=False,
            created_at=new_item.created_at,
            updated_at=new_item.updated_at
        )
        
        return CommonResponse(
            code=201,
            message="Menu item created successfully",
            message_id="MENU_ITEM_CREATED",
            data=response_item
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating menu item: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create menu item: {str(e)}"
        )


@router.put("/{item_id}", response_model=CommonResponse[MenuItemResponse])
async def update_menu_item(
    item_id: str,
    request: UpdateMenuItemRequest,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Update an existing menu item.
    
    Only updates fields that are provided in the request.
    """
    try:
        logger.info(f"Updating menu item {item_id} for owner: {current_user.user_id}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Get food item and verify ownership
        food_item = db.query(FoodItem).filter(
            and_(
                FoodItem.food_item_id == item_id,
                FoodItem.restaurant_id == restaurant.restaurant_id
            )
        ).first()
        
        if not food_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found or you don't have permission to edit it"
            )
        
        # Update fields if provided
        update_data = request.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == 'image_url':
                setattr(food_item, 'image', value)
            elif field == 'is_available':
                # Update status based on availability
                setattr(food_item, 'status', 'available' if value else 'unavailable')
            else:
                setattr(food_item, field, value)
        
        food_item.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(food_item)
        
        logger.info(f"Menu item updated successfully: {item_id}")
        
        # Get category name
        category_name = None
        if food_item.category_id:
            category = db.query(Category).filter(
                Category.category_id == food_item.category_id
            ).first()
            if category:
                category_name = category.name
        
        # Build response
        response_item = MenuItemResponse(
            food_item_id=str(food_item.food_item_id),
            name=food_item.name,
            description=food_item.description,
            price=float(food_item.price),
            discount_price=float(food_item.discount_price) if food_item.discount_price else None,
            category_id=str(food_item.category_id) if food_item.category_id else None,
            category_name=category_name,
            image=food_item.image,
            is_veg=food_item.is_veg,
            is_available=(food_item.status == 'available'),
            ingredients=food_item.ingredients,
            allergens=food_item.allergens,
            prep_time=food_item.prep_time,
            calories=food_item.calories,
            rating=float(food_item.rating) if food_item.rating else None,
            total_ratings=food_item.total_ratings,
            is_popular=food_item.is_popular,
            is_recommended=food_item.is_recommended,
            created_at=food_item.created_at,
            updated_at=food_item.updated_at
        )
        
        return CommonResponse(
            code=200,
            message="Menu item updated successfully",
            message_id="MENU_ITEM_UPDATED",
            data=response_item
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating menu item: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update menu item: {str(e)}"
        )


@router.delete("/{item_id}")
async def delete_menu_item(
    item_id: str,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Delete a menu item.
    
    Permanently removes the item from the database.
    """
    try:
        logger.info(f"Deleting menu item {item_id} for owner: {current_user.user_id}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Get food item and verify ownership
        food_item = db.query(FoodItem).filter(
            and_(
                FoodItem.food_item_id == item_id,
                FoodItem.restaurant_id == restaurant.restaurant_id
            )
        ).first()
        
        if not food_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found or you don't have permission to delete it"
            )
        
        # Delete the item
        db.delete(food_item)
        db.commit()
        
        logger.info(f"Menu item deleted successfully: {item_id}")
        
        return CommonResponse(
            code=200,
            message="Menu item deleted successfully",
            message_id="MENU_ITEM_DELETED",
            data={"deleted": True}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting menu item: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete menu item: {str(e)}"
        )


@router.put("/{item_id}/availability", response_model=CommonResponse[MenuItemResponse])
async def update_item_availability(
    item_id: str,
    request: UpdateItemAvailabilityRequest,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Toggle menu item availability (available/unavailable).
    
    This is a quick way to mark items as out of stock without deleting them.
    """
    try:
        logger.info(f"Updating availability for item {item_id}: {request.is_available}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Get food item and verify ownership
        food_item = db.query(FoodItem).filter(
            and_(
                FoodItem.food_item_id == item_id,
                FoodItem.restaurant_id == restaurant.restaurant_id
            )
        ).first()
        
        if not food_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found or you don't have permission to edit it"
            )
        
        # Update status
        food_item.status = 'available' if request.is_available else 'unavailable'
        food_item.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(food_item)
        
        logger.info(f"Item availability updated: {item_id} -> {food_item.status}")
        
        # Get category name
        category_name = None
        if food_item.category_id:
            category = db.query(Category).filter(
                Category.category_id == food_item.category_id
            ).first()
            if category:
                category_name = category.name
        
        # Build response
        response_item = MenuItemResponse(
            food_item_id=str(food_item.food_item_id),
            name=food_item.name,
            description=food_item.description,
            price=float(food_item.price),
            discount_price=float(food_item.discount_price) if food_item.discount_price else None,
            category_id=str(food_item.category_id) if food_item.category_id else None,
            category_name=category_name,
            image=food_item.image,
            is_veg=food_item.is_veg,
            is_available=request.is_available,
            ingredients=food_item.ingredients,
            allergens=food_item.allergens,
            prep_time=food_item.prep_time,
            calories=food_item.calories,
            rating=float(food_item.rating) if food_item.rating else None,
            total_ratings=food_item.total_ratings,
            is_popular=food_item.is_popular,
            is_recommended=food_item.is_recommended,
            created_at=food_item.created_at,
            updated_at=food_item.updated_at
        )
        
        return CommonResponse(
            code=200,
            message="Item availability updated successfully",
            message_id="AVAILABILITY_UPDATED",
            data=response_item
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating availability: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update availability: {str(e)}"
        )


# ============================================================================
# CATEGORY MANAGEMENT ENDPOINTS (OPTIONAL)
# ============================================================================

@router.get("/categories", response_model=CommonResponse[CategoryListResponse])
async def get_categories(
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Get all available categories.
    
    Returns list of categories that can be used when creating menu items.
    """
    try:
        # Get all active categories
        categories = db.query(Category).filter(
            Category.is_active == True
        ).order_by(Category.sort_order, Category.name).all()
        
        categories_response = [
            CategoryResponse(
                category_id=category.category_id,
                name=category.name,
                description=category.description,
                image=category.image,
                is_active=category.is_active,
                sort_order=category.sort_order
            )
            for category in categories
        ]
        
        return CommonResponse(
            code=200,
            message="Categories retrieved successfully",
            message_id="CATEGORIES_RETRIEVED",
            data=CategoryListResponse(
                categories=categories_response,
                total_count=len(categories_response)
            )
        )
    
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch categories: {str(e)}"
        )
