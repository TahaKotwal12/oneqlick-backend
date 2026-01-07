"""
Cart API Schemas
Pydantic models for cart-related requests and responses
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from enum import Enum


# ============================================================================
# REQUEST MODELS
# ============================================================================

class AddCartItemRequest(BaseModel):
    """Request to add item to cart"""
    food_item_id: UUID
    variant_id: Optional[UUID] = None
    quantity: int = Field(ge=1, le=99)
    special_instructions: Optional[str] = Field(None, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "food_item_id": "123e4567-e89b-12d3-a456-426614174000",
                "variant_id": "123e4567-e89b-12d3-a456-426614174001",
                "quantity": 2,
                "special_instructions": "Extra spicy"
            }
        }


class UpdateCartItemRequest(BaseModel):
    """Request to update cart item quantity"""
    cart_item_id: UUID
    quantity: int = Field(ge=0, le=99)  # 0 means remove
    
    class Config:
        json_schema_extra = {
            "example": {
                "cart_item_id": "123e4567-e89b-12d3-a456-426614174002",
                "quantity": 3
            }
        }


class RemoveCartItemRequest(BaseModel):
    """Request to remove item from cart"""
    cart_item_id: UUID
    
    class Config:
        json_schema_extra = {
            "example": {
                "cart_item_id": "123e4567-e89b-12d3-a456-426614174002"
            }
        }


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class CartItemResponse(BaseModel):
    """Single cart item response"""
    cart_item_id: UUID
    food_item_id: UUID
    food_item_name: str
    food_item_image: Optional[str] = None
    variant_id: Optional[UUID] = None
    variant_name: Optional[str] = None
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    special_instructions: Optional[str] = None
    is_veg: bool
    is_available: bool
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "cart_item_id": "123e4567-e89b-12d3-a456-426614174002",
                "food_item_id": "123e4567-e89b-12d3-a456-426614174000",
                "food_item_name": "Margherita Pizza",
                "food_item_image": "https://example.com/pizza.jpg",
                "variant_id": "123e4567-e89b-12d3-a456-426614174001",
                "variant_name": "Large",
                "quantity": 2,
                "unit_price": 299.00,
                "total_price": 598.00,
                "special_instructions": "Extra cheese",
                "is_veg": True,
                "is_available": True
            }
        }


class RestaurantBasicInfo(BaseModel):
    """Basic restaurant information"""
    restaurant_id: UUID
    name: str
    image: Optional[str] = None
    address_line1: str
    city: str
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Complete cart response with items and totals"""
    cart_id: UUID
    user_id: UUID
    restaurant_id: UUID
    restaurant: RestaurantBasicInfo
    items: List[CartItemResponse]
    item_count: int
    subtotal: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "cart_id": "123e4567-e89b-12d3-a456-426614174003",
                "user_id": "123e4567-e89b-12d3-a456-426614174004",
                "restaurant_id": "123e4567-e89b-12d3-a456-426614174005",
                "restaurant": {
                    "restaurant_id": "123e4567-e89b-12d3-a456-426614174005",
                    "name": "Pizza Palace",
                    "image": "https://example.com/restaurant.jpg",
                    "address_line1": "123 Main St",
                    "city": "Mumbai"
                },
                "items": [],
                "item_count": 2,
                "subtotal": 598.00,
                "created_at": "2024-01-07T12:00:00Z",
                "updated_at": "2024-01-07T12:30:00Z"
            }
        }


class CartSummaryResponse(BaseModel):
    """Quick cart summary"""
    cart_id: UUID
    item_count: int
    subtotal: Decimal
    restaurant_name: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "cart_id": "123e4567-e89b-12d3-a456-426614174003",
                "item_count": 3,
                "subtotal": 897.00,
                "restaurant_name": "Pizza Palace"
            }
        }


class CartItemAddedResponse(BaseModel):
    """Response after adding item to cart"""
    cart_id: UUID
    cart_item_id: UUID
    message: str
    cart_summary: CartSummaryResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "cart_id": "123e4567-e89b-12d3-a456-426614174003",
                "cart_item_id": "123e4567-e89b-12d3-a456-426614174002",
                "message": "Item added to cart successfully",
                "cart_summary": {
                    "cart_id": "123e4567-e89b-12d3-a456-426614174003",
                    "item_count": 3,
                    "subtotal": 897.00,
                    "restaurant_name": "Pizza Palace"
                }
            }
        }
