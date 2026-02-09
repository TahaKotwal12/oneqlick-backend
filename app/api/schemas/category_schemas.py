"""
Category schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    image: Optional[str] = Field(None, max_length=500, description="Category image URL")
    icon: Optional[str] = Field(None, max_length=100, description="Icon name for frontend")
    color: Optional[str] = Field(None, max_length=20, description="Hex color code (e.g., #FF5733)")
    is_active: bool = Field(True, description="Whether category is active")
    show_on_home: bool = Field(False, description="Show on home/search screens")
    sort_order: int = Field(0, description="Sort order for display")



class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    image: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    show_on_home: Optional[bool] = None
    sort_order: Optional[int] = None



class CategoryResponse(CategoryBase):
    """Schema for category response."""
    category_id: str = Field(..., description="Category UUID")
    created_at: datetime = Field(..., description="Creation timestamp")
    item_count: int = Field(0, description="Number of food items in this category")

    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    """Schema for list of categories."""
    categories: list[CategoryResponse]
    total_count: int = Field(..., description="Total number of categories")
