"""
Categories API routes for food categories management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import logging

from app.infra.db.postgres.postgres_config import get_db
from app.infra.db.postgres.models.category import Category
from app.infra.db.postgres.models.food_item import FoodItem
from app.api.schemas.category_schemas import (
    CategoryResponse,
    CategoryListResponse,
    CategoryCreate,
    CategoryUpdate
)
from app.api.schemas.common_schemas import CommonResponse

router = APIRouter(prefix="/categories", tags=["Categories"])
logger = logging.getLogger(__name__)


@router.get("", response_model=CommonResponse[CategoryListResponse])
async def get_categories(
    is_active: Optional[bool] = None,
    show_on_home: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get all food categories.
    
    Query Parameters:
    - is_active: Filter by active status (optional)
    - show_on_home: Filter by show_on_home flag (optional) - Use True to get only featured categories
    
    Returns list of categories with item counts, sorted by sort_order.
    """
    try:
        # Build query
        query = db.query(
            Category,
            func.count(FoodItem.food_item_id).label('item_count')
        ).outerjoin(
            FoodItem,
            Category.category_id == FoodItem.category_id
        ).group_by(Category.category_id)
        
        # Apply filters
        if is_active is not None:
            query = query.filter(Category.is_active == is_active)
        
        if show_on_home is not None:
            query = query.filter(Category.show_on_home == show_on_home)
        
        # Order by sort_order
        query = query.order_by(Category.sort_order, Category.name)
        
        # Execute query
        results = query.all()
        
        # Format response
        categories = []
        for category, item_count in results:
            category_dict = {
                "category_id": str(category.category_id),
                "name": category.name,
                "description": category.description,
                "image": category.image,
                "icon": category.icon,
                "color": category.color,
                "is_active": category.is_active,
                "show_on_home": category.show_on_home,
                "sort_order": category.sort_order,
                "created_at": category.created_at,
                "item_count": item_count or 0
            }
            categories.append(CategoryResponse(**category_dict))

        
        response_data = CategoryListResponse(
            categories=categories,
            total_count=len(categories)
        )
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Categories retrieved successfully",
            message_id="CATEGORIES_RETRIEVED",
            data=response_data
        )
        
    except Exception as e:
        logger.error(f"Error retrieving categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve categories: {str(e)}"
        )


@router.get("/{category_id}", response_model=CommonResponse[CategoryResponse])
async def get_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific category by ID.
    
    Path Parameters:
    - category_id: UUID of the category
    
    Returns category details with item count.
    """
    try:
        # Query category with item count
        result = db.query(
            Category,
            func.count(FoodItem.food_item_id).label('item_count')
        ).outerjoin(
            FoodItem,
            Category.category_id == FoodItem.category_id
        ).filter(
            Category.category_id == category_id
        ).group_by(Category.category_id).first()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        
        category, item_count = result
        
        category_dict = {
            "category_id": str(category.category_id),
            "name": category.name,
            "description": category.description,
            "image": category.image,
            "icon": category.icon,
            "color": category.color,
            "is_active": category.is_active,
            "show_on_home": category.show_on_home,
            "sort_order": category.sort_order,
            "created_at": category.created_at,
            "item_count": item_count or 0
        }
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Category retrieved successfully",
            message_id="CATEGORY_RETRIEVED",
            data=CategoryResponse(**category_dict)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving category {category_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve category: {str(e)}"
        )


@router.post("", response_model=CommonResponse[CategoryResponse], status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new food category.
    
    Request Body:
    - name: Category name (required)
    - description: Category description (optional)
    - image: Category image URL (optional)
    - is_active: Active status (default: true)
    - sort_order: Display order (default: 0)
    
    Returns the created category.
    """
    try:
        # Check if category with same name already exists
        existing = db.query(Category).filter(
            func.lower(Category.name) == category_data.name.lower()
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{category_data.name}' already exists"
            )
        
        # Create new category
        new_category = Category(
            name=category_data.name,
            description=category_data.description,
            image=category_data.image,
            is_active=category_data.is_active,
            sort_order=category_data.sort_order
        )
        
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        
        category_dict = {
            "category_id": str(new_category.category_id),
            "name": new_category.name,
            "description": new_category.description,
            "image": new_category.image,
            "icon": new_category.icon,
            "color": new_category.color,
            "is_active": new_category.is_active,
            "show_on_home": new_category.show_on_home,
            "sort_order": new_category.sort_order,
            "created_at": new_category.created_at,
            "item_count": 0
        }
        
        return CommonResponse(
            code=status.HTTP_201_CREATED,
            message="Category created successfully",
            message_id="CATEGORY_CREATED",
            data=CategoryResponse(**category_dict)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create category: {str(e)}"
        )


@router.put("/{category_id}", response_model=CommonResponse[CategoryResponse])
async def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing category.
    
    Path Parameters:
    - category_id: UUID of the category to update
    
    Request Body: (all fields optional)
    - name: Category name
    - description: Category description
    - image: Category image URL
    - is_active: Active status
    - sort_order: Display order
    
    Returns the updated category.
    """
    try:
        # Find category
        category = db.query(Category).filter(
            Category.category_id == category_id
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        
        # Update fields
        update_data = category_data.model_dump(exclude_unset=True)
        
        # Check for duplicate name if name is being updated
        if 'name' in update_data:
            existing = db.query(Category).filter(
                func.lower(Category.name) == update_data['name'].lower(),
                Category.category_id != category_id
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with name '{update_data['name']}' already exists"
                )
        
        for field, value in update_data.items():
            setattr(category, field, value)
        
        db.commit()
        db.refresh(category)
        
        # Get item count
        item_count = db.query(func.count(FoodItem.food_item_id)).filter(
            FoodItem.category_id == category_id
        ).scalar() or 0
        
        category_dict = {
            "category_id": str(category.category_id),
            "name": category.name,
            "description": category.description,
            "image": category.image,
            "icon": category.icon,
            "color": category.color,
            "is_active": category.is_active,
            "show_on_home": category.show_on_home,
            "sort_order": category.sort_order,
            "created_at": category.created_at,
            "item_count": item_count
        }
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Category updated successfully",
            message_id="CATEGORY_UPDATED",
            data=CategoryResponse(**category_dict)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating category {category_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update category: {str(e)}"
        )


@router.delete("/{category_id}", response_model=CommonResponse[dict])
async def delete_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a category.
    
    Path Parameters:
    - category_id: UUID of the category to delete
    
    Note: This will fail if there are food items associated with this category.
    """
    try:
        # Find category
        category = db.query(Category).filter(
            Category.category_id == category_id
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        
        # Check if category has food items
        item_count = db.query(func.count(FoodItem.food_item_id)).filter(
            FoodItem.category_id == category_id
        ).scalar() or 0
        
        if item_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete category with {item_count} associated food items. Please reassign or delete the items first."
            )
        
        db.delete(category)
        db.commit()
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Category deleted successfully",
            message_id="CATEGORY_DELETED",
            data={"category_id": category_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting category {category_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete category: {str(e)}"
        )
