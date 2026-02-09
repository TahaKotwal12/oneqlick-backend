# OneQlick Backend - Missing APIs Implementation Guide

**Document Version:** 1.0  
**Date:** January 3, 2026  
**Purpose:** Detailed implementation guide for missing backend APIs

---

## Table of Contents

1. [Phase 1: Critical APIs](#phase-1-critical-apis)
   - [Cart Management APIs](#cart-management-apis)
   - [Order Management APIs](#order-management-apis)
   - [Payment APIs](#payment-apis)
2. [Phase 2: User Experience APIs](#phase-2-user-experience-apis)
3. [Phase 3: Advanced Features](#phase-3-advanced-features)
4. [Implementation Standards](#implementation-standards)
5. [Testing Guidelines](#testing-guidelines)

---

## Phase 1: Critical APIs

### Cart Management APIs

#### 1.1 Get or Create Cart
```
GET /cart
```

**Description:** Get the current user's active cart or create a new one if none exists.

**Request:**
- Headers: `Authorization: Bearer {token}`

**Response:**
```json
{
  "success": true,
  "data": {
    "cart_id": "uuid",
    "user_id": "uuid",
    "restaurant_id": "uuid",
    "restaurant": {
      "restaurant_id": "uuid",
      "name": "Restaurant Name",
      "image": "url",
      "min_order_amount": 100.00,
      "delivery_fee": 30.00
    },
    "items": [
      {
        "cart_item_id": "uuid",
        "food_item_id": "uuid",
        "food_item": {
          "name": "Item Name",
          "price": 150.00,
          "image": "url",
          "is_veg": true
        },
        "quantity": 2,
        "customizations": [
          {
            "customization_id": "uuid",
            "name": "Spice Level",
            "option_id": "uuid",
            "option_name": "Medium",
            "price_adjustment": 0
          }
        ],
        "addons": [
          {
            "addon_id": "uuid",
            "name": "Extra Cheese",
            "quantity": 1,
            "price": 30.00
          }
        ],
        "special_instructions": "No onions",
        "item_total": 360.00
      }
    ],
    "subtotal": 360.00,
    "tax_amount": 18.00,
    "delivery_fee": 30.00,
    "discount_amount": 0.00,
    "total_amount": 408.00,
    "item_count": 2,
    "created_at": "2026-01-03T12:00:00Z",
    "updated_at": "2026-01-03T12:05:00Z"
  }
}
```

**Implementation:**
```python
# File: app/api/routes/cart.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.cart import Cart, CartItem
from app.api.schemas.cart_schemas import CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("", response_model=CartResponse)
async def get_or_create_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's active cart or create new one"""
    
    # Check for existing active cart
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id
    ).first()
    
    if not cart:
        # Create new cart
        cart = Cart(user_id=current_user.user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Calculate cart totals
    cart_data = calculate_cart_totals(cart, db)
    
    return {
        "success": True,
        "data": cart_data
    }
```

---

#### 1.2 Add Item to Cart
```
POST /cart/items
```

**Description:** Add a food item to the cart with customizations and add-ons.

**Request Body:**
```json
{
  "food_item_id": "uuid",
  "restaurant_id": "uuid",
  "quantity": 2,
  "customizations": [
    {
      "customization_id": "uuid",
      "option_id": "uuid"
    }
  ],
  "addons": [
    {
      "addon_id": "uuid",
      "quantity": 1
    }
  ],
  "special_instructions": "No onions"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "cart_item_id": "uuid",
    "message": "Item added to cart successfully"
  }
}
```

**Business Logic:**
1. Validate food item exists and is available
2. Check if cart exists for user
3. If cart has items from different restaurant, clear cart or show error
4. Validate customizations and add-ons
5. Check if same item with same customizations exists (update quantity)
6. Add item to cart
7. Return updated cart

**Implementation:**
```python
@router.post("/items", response_model=CartItemResponse)
async def add_item_to_cart(
    request: AddCartItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add item to cart with customizations and add-ons"""
    
    # Validate food item
    food_item = db.query(FoodItem).filter(
        FoodItem.food_item_id == request.food_item_id,
        FoodItem.status == FoodStatus.AVAILABLE
    ).first()
    
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found or unavailable"
        )
    
    # Get or create cart
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id
    ).first()
    
    if not cart:
        cart = Cart(
            user_id=current_user.user_id,
            restaurant_id=request.restaurant_id
        )
        db.add(cart)
        db.flush()
    
    # Check if cart has items from different restaurant
    if cart.restaurant_id and cart.restaurant_id != request.restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add items from different restaurant. Clear cart first."
        )
    
    # Update cart restaurant if not set
    if not cart.restaurant_id:
        cart.restaurant_id = request.restaurant_id
    
    # Check for existing item with same customizations
    existing_item = find_matching_cart_item(
        cart.cart_id, 
        request.food_item_id,
        request.customizations,
        request.addons,
        db
    )
    
    if existing_item:
        # Update quantity
        existing_item.quantity += request.quantity
        db.commit()
        return {
            "success": True,
            "data": {
                "cart_item_id": existing_item.cart_item_id,
                "message": "Item quantity updated"
            }
        }
    
    # Create new cart item
    cart_item = CartItem(
        cart_id=cart.cart_id,
        food_item_id=request.food_item_id,
        quantity=request.quantity,
        special_instructions=request.special_instructions
    )
    db.add(cart_item)
    db.flush()
    
    # Add customizations
    for custom in request.customizations:
        cart_custom = CartItemCustomization(
            cart_item_id=cart_item.cart_item_id,
            customization_id=custom.customization_id,
            option_id=custom.option_id
        )
        db.add(cart_custom)
    
    # Add add-ons
    for addon in request.addons:
        cart_addon = CartItemAddon(
            cart_item_id=cart_item.cart_item_id,
            addon_id=addon.addon_id,
            quantity=addon.quantity
        )
        db.add(cart_addon)
    
    db.commit()
    db.refresh(cart_item)
    
    return {
        "success": True,
        "data": {
            "cart_item_id": cart_item.cart_item_id,
            "message": "Item added to cart successfully"
        }
    }
```

---

#### 1.3 Update Cart Item
```
PUT /cart/items/{cart_item_id}
```

**Request Body:**
```json
{
  "quantity": 3,
  "special_instructions": "Extra spicy"
}
```

---

#### 1.4 Remove Cart Item
```
DELETE /cart/items/{cart_item_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Item removed from cart"
  }
}
```

---

#### 1.5 Clear Cart
```
DELETE /cart
```

**Description:** Remove all items from cart.

---

#### 1.6 Validate Cart
```
POST /cart/validate
```

**Description:** Validate cart before checkout (check availability, prices, minimum order).

**Response:**
```json
{
  "success": true,
  "data": {
    "is_valid": true,
    "errors": [],
    "warnings": [
      "Delivery fee has changed from ₹30 to ₹40"
    ],
    "cart_summary": {
      "subtotal": 360.00,
      "total": 418.00
    }
  }
}
```

---

### Order Management APIs

#### 2.1 Create Order
```
POST /orders
```

**Description:** Create a new order from cart.

**Request Body:**
```json
{
  "delivery_address_id": "uuid",
  "payment_method": "card",
  "special_instructions": "Ring doorbell",
  "coupon_code": "SAVE20",
  "scheduled_delivery_time": null
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "order_id": "uuid",
    "order_number": "OQ20260103001",
    "status": "pending",
    "payment_status": "pending",
    "total_amount": 418.00,
    "estimated_delivery_time": "2026-01-03T13:30:00Z",
    "payment_details": {
      "payment_id": "pay_xyz123",
      "payment_url": "https://payment-gateway.com/pay/xyz123"
    }
  }
}
```

**Business Logic:**
1. Validate cart is not empty
2. Validate delivery address
3. Validate coupon if provided
4. Calculate final amounts
5. Create order record
6. Create order items from cart items
7. Initiate payment
8. Clear cart on success
9. Send order confirmation notification

**Implementation:**
```python
@router.post("", response_model=OrderResponse)
async def create_order(
    request: CreateOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new order from cart"""
    
    # Get user's cart
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id
    ).first()
    
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Validate delivery address
    address = db.query(Address).filter(
        Address.address_id == request.delivery_address_id,
        Address.user_id == current_user.user_id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery address not found"
        )
    
    # Calculate order totals
    order_totals = calculate_order_totals(cart, request.coupon_code, db)
    
    # Generate order number
    order_number = generate_order_number()
    
    # Create order
    order = Order(
        customer_id=current_user.user_id,
        restaurant_id=cart.restaurant_id,
        delivery_address_id=request.delivery_address_id,
        order_number=order_number,
        subtotal=order_totals['subtotal'],
        tax_amount=order_totals['tax_amount'],
        delivery_fee=order_totals['delivery_fee'],
        discount_amount=order_totals['discount_amount'],
        total_amount=order_totals['total_amount'],
        payment_method=request.payment_method,
        payment_status=PaymentStatus.PENDING,
        order_status=OrderStatus.PENDING,
        special_instructions=request.special_instructions,
        estimated_delivery_time=calculate_eta(cart.restaurant_id, address)
    )
    db.add(order)
    db.flush()
    
    # Create order items from cart
    for cart_item in cart.items:
        order_item = OrderItem(
            order_id=order.order_id,
            food_item_id=cart_item.food_item_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.food_item.price,
            total_price=cart_item.food_item.price * cart_item.quantity,
            special_instructions=cart_item.special_instructions
        )
        db.add(order_item)
        db.flush()
        
        # Copy customizations
        for custom in cart_item.customizations:
            order_custom = OrderItemCustomization(
                order_item_id=order_item.order_item_id,
                customization_id=custom.customization_id,
                option_id=custom.option_id
            )
            db.add(order_custom)
        
        # Copy add-ons
        for addon in cart_item.addons:
            order_addon = OrderItemAddon(
                order_item_id=order_item.order_item_id,
                addon_id=addon.addon_id,
                quantity=addon.quantity
            )
            db.add(order_addon)
    
    # Initiate payment
    payment_result = initiate_payment(order, request.payment_method)
    order.payment_id = payment_result['payment_id']
    
    # Create order tracking entry
    tracking = OrderTracking(
        order_id=order.order_id,
        status=OrderStatus.PENDING,
        notes="Order placed successfully"
    )
    db.add(tracking)
    
    # Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()
    
    db.commit()
    db.refresh(order)
    
    # Send notification
    send_order_notification(order, current_user)
    
    return {
        "success": True,
        "data": {
            "order_id": order.order_id,
            "order_number": order.order_number,
            "status": order.order_status,
            "payment_status": order.payment_status,
            "total_amount": order.total_amount,
            "estimated_delivery_time": order.estimated_delivery_time,
            "payment_details": payment_result
        }
    }
```

---

#### 2.2 Get Orders List
```
GET /orders?status={status}&page={page}&limit={limit}
```

**Query Parameters:**
- `status` (optional): Filter by order status
- `page` (default: 1): Page number
- `limit` (default: 20): Items per page

**Response:**
```json
{
  "success": true,
  "data": {
    "orders": [
      {
        "order_id": "uuid",
        "order_number": "OQ20260103001",
        "restaurant": {
          "name": "Restaurant Name",
          "image": "url"
        },
        "status": "delivered",
        "payment_status": "paid",
        "total_amount": 418.00,
        "item_count": 3,
        "created_at": "2026-01-03T12:00:00Z",
        "delivered_at": "2026-01-03T13:25:00Z"
      }
    ],
    "total_count": 45,
    "page": 1,
    "page_size": 20,
    "has_more": true
  }
}
```

---

#### 2.3 Get Order Details
```
GET /orders/{order_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "order_id": "uuid",
    "order_number": "OQ20260103001",
    "status": "delivered",
    "payment_status": "paid",
    "restaurant": {
      "restaurant_id": "uuid",
      "name": "Restaurant Name",
      "phone": "+91 1234567890",
      "image": "url"
    },
    "delivery_address": {
      "title": "Home",
      "address_line1": "123 Main St",
      "city": "Mumbai",
      "postal_code": "400001"
    },
    "items": [
      {
        "food_item": {
          "name": "Margherita Pizza",
          "image": "url"
        },
        "quantity": 2,
        "unit_price": 150.00,
        "total_price": 300.00,
        "customizations": [],
        "addons": []
      }
    ],
    "subtotal": 360.00,
    "tax_amount": 18.00,
    "delivery_fee": 40.00,
    "discount_amount": 0.00,
    "total_amount": 418.00,
    "payment_method": "card",
    "special_instructions": "Ring doorbell",
    "estimated_delivery_time": "2026-01-03T13:30:00Z",
    "actual_delivery_time": "2026-01-03T13:25:00Z",
    "created_at": "2026-01-03T12:00:00Z",
    "tracking_history": [
      {
        "status": "pending",
        "timestamp": "2026-01-03T12:00:00Z",
        "notes": "Order placed"
      },
      {
        "status": "confirmed",
        "timestamp": "2026-01-03T12:05:00Z",
        "notes": "Order confirmed by restaurant"
      }
    ]
  }
}
```

---

#### 2.4 Cancel Order
```
POST /orders/{order_id}/cancel
```

**Request Body:**
```json
{
  "reason": "Changed my mind"
}
```

**Business Logic:**
1. Check if order can be cancelled (status must be pending/confirmed)
2. Update order status to cancelled
3. Initiate refund if payment was made
4. Send cancellation notification
5. Update restaurant and delivery partner

---

#### 2.5 Track Order
```
GET /orders/{order_id}/track
```

**Response:**
```json
{
  "success": true,
  "data": {
    "order_id": "uuid",
    "order_number": "OQ20260103001",
    "current_status": "out_for_delivery",
    "estimated_delivery_time": "2026-01-03T13:30:00Z",
    "delivery_partner": {
      "name": "John Doe",
      "phone": "+91 9876543210",
      "vehicle_number": "MH01AB1234",
      "rating": 4.8
    },
    "current_location": {
      "latitude": 19.0760,
      "longitude": 72.8777
    },
    "delivery_address": {
      "latitude": 19.0896,
      "longitude": 72.8656
    },
    "distance_remaining_km": 2.5,
    "eta_minutes": 15,
    "status_history": [
      {
        "status": "pending",
        "timestamp": "2026-01-03T12:00:00Z"
      },
      {
        "status": "confirmed",
        "timestamp": "2026-01-03T12:05:00Z"
      },
      {
        "status": "preparing",
        "timestamp": "2026-01-03T12:10:00Z"
      },
      {
        "status": "ready_for_pickup",
        "timestamp": "2026-01-03T12:45:00Z"
      },
      {
        "status": "picked_up",
        "timestamp": "2026-01-03T13:00:00Z"
      },
      {
        "status": "out_for_delivery",
        "timestamp": "2026-01-03T13:05:00Z"
      }
    ]
  }
}
```

---

### Payment APIs

#### 3.1 Get Payment Methods
```
GET /payment/methods
```

**Response:**
```json
{
  "success": true,
  "data": {
    "payment_methods": [
      {
        "payment_method_id": "uuid",
        "payment_type": "card",
        "name": "HDFC Credit Card",
        "last_four_digits": "1234",
        "is_default": true,
        "is_active": true
      },
      {
        "payment_method_id": "uuid",
        "payment_type": "upi",
        "name": "Google Pay",
        "upi_id": "user@oksbi",
        "is_default": false,
        "is_active": true
      }
    ]
  }
}
```

---

#### 3.2 Add Payment Method
```
POST /payment/methods
```

**Request Body:**
```json
{
  "payment_type": "card",
  "name": "HDFC Credit Card",
  "card_token": "tok_xyz123",
  "is_default": true
}
```

---

#### 3.3 Initiate Payment
```
POST /payment/initiate
```

**Request Body:**
```json
{
  "order_id": "uuid",
  "payment_method_id": "uuid",
  "amount": 418.00
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "payment_id": "pay_xyz123",
    "payment_url": "https://payment-gateway.com/pay/xyz123",
    "status": "initiated",
    "expires_at": "2026-01-03T12:15:00Z"
  }
}
```

---

#### 3.4 Verify Payment
```
POST /payment/verify
```

**Request Body:**
```json
{
  "payment_id": "pay_xyz123",
  "payment_signature": "signature_hash"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "payment_id": "pay_xyz123",
    "status": "success",
    "order_id": "uuid",
    "amount": 418.00,
    "verified_at": "2026-01-03T12:10:00Z"
  }
}
```

---

## Phase 2: User Experience APIs

### Favorites APIs

#### 4.1 Get Favorites
```
GET /favorites
```

#### 4.2 Add to Favorites
```
POST /favorites/{restaurant_id}
```

#### 4.3 Remove from Favorites
```
DELETE /favorites/{restaurant_id}
```

#### 4.4 Check Favorite Status
```
GET /favorites/check/{restaurant_id}
```

---

### Notifications APIs

#### 5.1 Get Notifications
```
GET /notifications?page={page}&limit={limit}&unread_only={bool}
```

#### 5.2 Mark as Read
```
PUT /notifications/{notification_id}/read
```

#### 5.3 Mark All as Read
```
PUT /notifications/read-all
```

#### 5.4 Delete Notification
```
DELETE /notifications/{notification_id}
```

---

### Coupons APIs

#### 6.1 Get Available Coupons
```
GET /coupons?restaurant_id={uuid}
```

#### 6.2 Validate Coupon
```
POST /coupons/validate
```

**Request Body:**
```json
{
  "coupon_code": "SAVE20",
  "cart_total": 360.00,
  "restaurant_id": "uuid"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "is_valid": true,
    "coupon": {
      "code": "SAVE20",
      "title": "Save 20% on orders above ₹300",
      "discount_type": "percentage",
      "discount_value": 20.00,
      "max_discount_amount": 100.00
    },
    "discount_amount": 72.00,
    "final_amount": 288.00
  }
}
```

---

## Implementation Standards

### 1. File Structure
```
app/
├── api/
│   ├── routes/
│   │   ├── cart.py          # Cart management
│   │   ├── orders.py        # Order management
│   │   ├── payment.py       # Payment APIs
│   │   ├── favorites.py     # Favorites
│   │   ├── notifications.py # Notifications
│   │   └── coupons.py       # Coupons
│   └── schemas/
│       ├── cart_schemas.py
│       ├── order_schemas.py
│       ├── payment_schemas.py
│       └── ...
├── infra/
│   └── db/
│       └── postgres/
│           └── models/
│               ├── cart.py
│               ├── order.py
│               └── ...
└── services/
    ├── cart_service.py
    ├── order_service.py
    ├── payment_service.py
    └── notification_service.py
```

### 2. Schema Naming Convention
- Request schemas: `{Entity}CreateRequest`, `{Entity}UpdateRequest`
- Response schemas: `{Entity}Response`, `{Entity}ListResponse`
- Example: `CartItemCreateRequest`, `OrderResponse`

### 3. Error Handling
```python
from fastapi import HTTPException, status

# Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid request data"
)

# Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Authentication required"
)

# Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Access denied"
)
```

### 4. Response Format
```python
# Success Response
{
    "success": True,
    "data": {...},
    "statusCode": 200
}

# Error Response
{
    "success": False,
    "error": "Error message",
    "statusCode": 400
}
```

### 5. Pagination
```python
from fastapi import Query

@router.get("")
async def get_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    
    items = db.query(Model)\
        .offset(offset)\
        .limit(page_size)\
        .all()
    
    total_count = db.query(Model).count()
    
    return {
        "success": True,
        "data": {
            "items": items,
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "has_more": (page * page_size) < total_count
        }
    }
```

---

## Testing Guidelines

### 1. Unit Tests
```python
# tests/test_cart.py

import pytest
from fastapi.testclient import TestClient

def test_add_item_to_cart(client: TestClient, auth_headers):
    response = client.post(
        "/cart/items",
        json={
            "food_item_id": "uuid",
            "restaurant_id": "uuid",
            "quantity": 2
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "cart_item_id" in response.json()["data"]

def test_add_item_invalid_food_item(client: TestClient, auth_headers):
    response = client.post(
        "/cart/items",
        json={
            "food_item_id": "invalid-uuid",
            "restaurant_id": "uuid",
            "quantity": 2
        },
        headers=auth_headers
    )
    
    assert response.status_code == 404
```

### 2. Integration Tests
```python
def test_complete_order_flow(client: TestClient, auth_headers):
    # 1. Add items to cart
    cart_response = client.post("/cart/items", ...)
    assert cart_response.status_code == 200
    
    # 2. Validate cart
    validate_response = client.post("/cart/validate")
    assert validate_response.json()["data"]["is_valid"] == True
    
    # 3. Create order
    order_response = client.post("/orders", ...)
    assert order_response.status_code == 200
    order_id = order_response.json()["data"]["order_id"]
    
    # 4. Verify payment
    payment_response = client.post("/payment/verify", ...)
    assert payment_response.status_code == 200
    
    # 5. Check order status
    status_response = client.get(f"/orders/{order_id}")
    assert status_response.json()["data"]["payment_status"] == "paid"
```

---

## Next Steps

1. **Week 1:**
   - Implement Cart Management APIs (1.1 - 1.6)
   - Write unit tests for cart operations
   - Test cart integration with User App

2. **Week 2:**
   - Implement Order Management APIs (2.1 - 2.5)
   - Implement Payment APIs (3.1 - 3.4)
   - Integration testing

3. **Week 3-4:**
   - Implement Phase 2 APIs (Favorites, Notifications, Coupons)
   - End-to-end testing

4. **Week 5-6:**
   - Implement Phase 3 APIs (Wallet, Preferences, etc.)
   - Performance optimization
   - Documentation

---

**Document End**
