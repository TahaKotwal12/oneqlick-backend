# 🔐 OneQlick Backend - Partner API Development Guide

## **📚 Table of Contents**
1. [Authentication Flow](#authentication-flow)
2. [API Structure & Patterns](#api-structure--patterns)
3. [Partner API Specifications](#partner-api-specifications)
4. [Implementation Steps](#implementation-steps)

---

## **🔐 Authentication Flow**

### **How Authentication Works:**

```
1. USER LOGS IN
   ├─> POST /api/v1/auth/login
   ├─> Body: { email, password }
   └─> Returns: { user, tokens: { access_token, refresh_token } }

2. ACCESS TOKEN (JWT)
   ├─> Stored in: Authorization header
   ├─> Format: "Bearer <access_token>"
   ├─> Contains: { user_id, role }
   ├─> Expires: 24 hours (configurable)
   └─> Used for: All authenticated requests

3. REFRESH TOKEN
   ├─> Stored in: Client storage (secure)
   ├─> Hashed in: Database (RefreshToken table)
   ├─> Expires: 30 days
   └─> Used for: Getting new access tokens

4. PROTECTED ENDPOINTS
   ├─> Require: Authorization header with valid JWT
   ├─> Dependency: get_current_user()
   ├─> Validates: Token signature, expiry, user status
   └─> Returns: User object
```

### **Role-Based Access Control:**

```python
# In dependencies.py
require_restaurant_owner = require_roles("restaurant_owner")
require_delivery_partner = require_roles("delivery_partner")

# Usage in routes
@router.get("/orders")
async def get_orders(
    current_user: User = Depends(require_restaurant_owner),  # ✅ Only restaurant owners
    db: Session = Depends(get_db)
):
    # User is guaranteed to be a restaurant owner
    pass
```

### **User Roles in Database:**
```sql
CREATE TYPE user_role AS ENUM (
    'customer',           -- Regular app users
    'admin',             -- Platform administrators
    'delivery_partner',  -- Delivery drivers
    'restaurant_owner'   -- Restaurant managers
);
```

---

## **🏗️ API Structure & Patterns**

### **1. Standard Response Format:**

All APIs use `CommonResponse[T]` wrapper:

```python
from app.api.schemas.common_schemas import CommonResponse

# Success Response
return CommonResponse(
    code=200,
    message="Operation successful",
    message_id="OPERATION_SUCCESS",
    data=YourDataSchema(...)
)

# Error Response (via HTTPException)
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Error message"
)
```

### **2. File Structure:**

```
app/
├── api/
│   ├── routes/
│   │   ├── auth.py                    # ✅ Existing
│   │   ├── user.py                    # ✅ Existing
│   │   ├── restaurant.py              # ✅ Existing (customer-facing)
│   │   ├── partner_restaurant.py      # 🆕 NEW - Restaurant owner APIs
│   │   └── partner_delivery.py        # 🆕 NEW - Delivery partner APIs
│   ├── schemas/
│   │   ├── common_schemas.py          # ✅ Existing
│   │   ├── auth_schemas.py            # ✅ Existing
│   │   ├── partner_restaurant_schemas.py  # 🆕 NEW
│   │   └── partner_delivery_schemas.py    # 🆕 NEW
│   └── dependencies.py                # ✅ Existing (has role checkers)
├── infra/db/postgres/models/
│   ├── user.py                        # ✅ Existing
│   ├── order.py                       # ✅ Existing
│   ├── food_item.py                   # ✅ Existing
│   ├── delivery_partner.py            # ✅ Existing
│   └── restaurant.py                  # ✅ Existing
└── utils/
    └── enums.py                       # ✅ Existing (OrderStatus, etc.)
```

### **3. Request/Response Pattern:**

```python
# 1. Define Request Schema (what client sends)
class UpdateOrderStatusRequest(BaseModel):
    status: str  # 'preparing', 'ready', 'rejected'

# 2. Define Response Schema (what API returns)
class OrderResponse(BaseModel):
    order_id: UUID
    order_number: str
    customer_name: str
    total_amount: Decimal
    status: str
    created_at: datetime

# 3. Define API Endpoint
@router.put("/orders/{order_id}/status", response_model=CommonResponse[OrderResponse])
async def update_order_status(
    order_id: str,
    request: UpdateOrderStatusRequest,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    # Implementation
    pass
```

---

## **📋 Partner API Specifications**

### **PHASE 1: Restaurant Owner - Order Management**

#### **1.1 Get All Orders**
```python
GET /api/v1/partner/restaurant/orders

Headers:
  Authorization: Bearer <access_token>

Query Parameters:
  status: Optional[str] = None  # 'pending', 'preparing', 'ready', 'delivered'
  limit: int = 50
  offset: int = 0

Response:
{
  "code": 200,
  "message": "Orders retrieved successfully",
  "message_id": "ORDERS_RETRIEVED",
  "data": {
    "orders": [
      {
        "order_id": "uuid",
        "order_number": "ORD-1001",
        "customer_name": "John Doe",
        "customer_phone": "+91-9876543210",
        "total_amount": 450.00,
        "order_status": "pending",
        "payment_status": "paid",
        "payment_method": "upi",
        "created_at": "2026-01-04T12:00:00Z",
        "estimated_delivery_time": "2026-01-04T13:00:00Z",
        "special_instructions": "Extra spicy",
        "items": [
          {
            "food_item_id": "uuid",
            "name": "Butter Chicken",
            "quantity": 2,
            "price": 200.00,
            "customizations": ["Extra gravy"],
            "addons": ["Naan"]
          }
        ],
        "delivery_address": {
          "address_line1": "123 Main St",
          "city": "Mumbai",
          "postal_code": "400001"
        }
      }
    ],
    "total_count": 45,
    "has_more": true
  }
}
```

#### **1.2 Get Order Details**
```python
GET /api/v1/partner/restaurant/orders/{order_id}

Headers:
  Authorization: Bearer <access_token>

Response:
{
  "code": 200,
  "message": "Order details retrieved",
  "message_id": "ORDER_DETAILS_SUCCESS",
  "data": {
    # Same as order object above with full details
  }
}
```

#### **1.3 Update Order Status**
```python
PUT /api/v1/partner/restaurant/orders/{order_id}/status

Headers:
  Authorization: Bearer <access_token>

Body:
{
  "status": "preparing"  # 'preparing', 'ready', 'rejected'
}

Response:
{
  "code": 200,
  "message": "Order status updated successfully",
  "message_id": "ORDER_STATUS_UPDATED",
  "data": {
    # Updated order object
  }
}
```

#### **1.4 Add Order Notes**
```python
POST /api/v1/partner/restaurant/orders/{order_id}/notes

Headers:
  Authorization: Bearer <access_token>

Body:
{
  "note": "Customer requested extra packaging"
}

Response:
{
  "code": 200,
  "message": "Note added successfully",
  "message_id": "NOTE_ADDED",
  "data": {
    "note_id": "uuid",
    "note": "Customer requested extra packaging",
    "created_at": "2026-01-04T12:30:00Z"
  }
}
```

#### **1.5 Get Restaurant Statistics**
```python
GET /api/v1/partner/restaurant/stats

Headers:
  Authorization: Bearer <access_token>

Response:
{
  "code": 200,
  "message": "Statistics retrieved",
  "message_id": "STATS_SUCCESS",
  "data": {
    "today_orders": 12,
    "pending_orders": 3,
    "revenue_today": 5400.00,
    "avg_preparation_time": 25,  # minutes
    "total_orders_this_month": 345,
    "revenue_this_month": 152000.00
  }
}
```

---

### **PHASE 1: Restaurant Owner - Menu Management**

#### **2.1 Get Menu Items**
```python
GET /api/v1/partner/restaurant/menu

Headers:
  Authorization: Bearer <access_token>

Query Parameters:
  category_id: Optional[str] = None
  is_available: Optional[bool] = None
  search: Optional[str] = None

Response:
{
  "code": 200,
  "message": "Menu items retrieved",
  "message_id": "MENU_SUCCESS",
  "data": {
    "items": [
      {
        "food_item_id": "uuid",
        "name": "Butter Chicken",
        "description": "Rich and creamy chicken curry",
        "price": 280.00,
        "discount_price": null,
        "category_id": "uuid",
        "category_name": "Main Course",
        "image": "https://...",
        "is_veg": false,
        "is_available": true,
        "ingredients": "Chicken, Butter, Cream, Spices",
        "allergens": "Dairy",
        "prep_time": 20,
        "calories": 450,
        "rating": 4.5,
        "total_ratings": 120,
        "is_popular": true,
        "created_at": "2026-01-01T00:00:00Z"
      }
    ],
    "total_count": 45
  }
}
```

#### **2.2 Create Menu Item**
```python
POST /api/v1/partner/restaurant/menu

Headers:
  Authorization: Bearer <access_token>

Body:
{
  "name": "Paneer Tikka",
  "description": "Grilled cottage cheese with spices",
  "price": 220.00,
  "category_id": "uuid",
  "is_veg": true,
  "image_url": "https://...",
  "ingredients": "Paneer, Spices, Yogurt",
  "allergens": "Dairy",
  "prep_time": 15,
  "calories": 320
}

Response:
{
  "code": 201,
  "message": "Menu item created successfully",
  "message_id": "MENU_ITEM_CREATED",
  "data": {
    # Created food item object
  }
}
```

#### **2.3 Update Menu Item**
```python
PUT /api/v1/partner/restaurant/menu/{item_id}

Headers:
  Authorization: Bearer <access_token>

Body:
{
  "name": "Paneer Tikka (Updated)",
  "price": 240.00,
  "description": "Updated description",
  "image_url": "https://new-image.jpg"
}

Response:
{
  "code": 200,
  "message": "Menu item updated",
  "message_id": "MENU_ITEM_UPDATED",
  "data": {
    # Updated food item
  }
}
```

#### **2.4 Delete Menu Item**
```python
DELETE /api/v1/partner/restaurant/menu/{item_id}

Headers:
  Authorization: Bearer <access_token>

Response:
{
  "code": 200,
  "message": "Menu item deleted",
  "message_id": "MENU_ITEM_DELETED",
  "data": {
    "deleted": true
  }
}
```

#### **2.5 Toggle Item Availability**
```python
PUT /api/v1/partner/restaurant/menu/{item_id}/availability

Headers:
  Authorization: Bearer <access_token>

Body:
{
  "is_available": false
}

Response:
{
  "code": 200,
  "message": "Availability updated",
  "message_id": "AVAILABILITY_UPDATED",
  "data": {
    # Updated food item
  }
}
```

---

### **PHASE 2: Delivery Partner APIs**

#### **3.1 Get Available Delivery Requests**
```python
GET /api/v1/partner/delivery/requests

Headers:
  Authorization: Bearer <access_token>

Query Parameters:
  nearby: bool = true  # Filter by location

Response:
{
  "code": 200,
  "message": "Delivery requests retrieved",
  "message_id": "REQUESTS_SUCCESS",
  "data": {
    "requests": [
      {
        "order_id": "uuid",
        "order_number": "ORD-1001",
        "amount": 450.00,
        "restaurant": {
          "name": "Spice Kitchen",
          "address": "123 Food St",
          "latitude": 19.0760,
          "longitude": 72.8777
        },
        "customer": {
          "name": "John Doe",
          "phone": "+91-9876543210",
          "address": "456 Home St",
          "latitude": 19.0820,
          "longitude": 72.8850
        },
        "payment_type": "upi",
        "distance": 3.5,  # km
        "estimated_time": 25,  # minutes
        "created_at": "2026-01-04T12:00:00Z"
      }
    ],
    "total_count": 5
  }
}
```

#### **3.2 Accept Delivery Request**
```python
POST /api/v1/partner/delivery/requests/{order_id}/accept

Headers:
  Authorization: Bearer <access_token>

Response:
{
  "code": 200,
  "message": "Delivery accepted",
  "message_id": "DELIVERY_ACCEPTED",
  "data": {
    # Full order details
  }
}
```

#### **3.3 Update Delivery Status**
```python
PUT /api/v1/partner/delivery/orders/{order_id}/status

Headers:
  Authorization: Bearer <access_token>

Body:
{
  "status": "picked_up",  # 'picked_up', 'delivered'
  "latitude": 19.0760,
  "longitude": 72.8777
}

Response:
{
  "code": 200,
  "message": "Status updated",
  "message_id": "STATUS_UPDATED",
  "data": {
    # Updated order
  }
}
```

#### **3.4 Update Location**
```python
POST /api/v1/partner/delivery/location

Headers:
  Authorization: Bearer <access_token>

Body:
{
  "latitude": 19.0760,
  "longitude": 72.8777
}

Response:
{
  "code": 200,
  "message": "Location updated",
  "message_id": "LOCATION_UPDATED",
  "data": {
    "updated": true
  }
}
```

#### **3.5 Toggle Availability**
```python
PUT /api/v1/partner/delivery/availability

Headers:
  Authorization: Bearer <access_token>

Body:
{
  "is_online": true
}

Response:
{
  "code": 200,
  "message": "Availability updated",
  "message_id": "AVAILABILITY_UPDATED",
  "data": {
    "is_online": true
  }
}
```

---

## **🚀 Implementation Steps**

### **Step 1: Create Schema Files**

1. Create `partner_restaurant_schemas.py`
2. Create `partner_delivery_schemas.py`
3. Define all request/response models

### **Step 2: Create Route Files**

1. Create `partner_restaurant.py`
2. Create `partner_delivery.py`
3. Implement endpoints with role-based access

### **Step 3: Register Routes**

Update `app/main.py`:
```python
from app.api.routes import partner_restaurant, partner_delivery

app.include_router(partner_restaurant.router, prefix="/api/v1/partner")
app.include_router(partner_delivery.router, prefix="/api/v1/partner")
```

### **Step 4: Test with Partner App**

1. Update `partnerService.ts` to call real APIs
2. Test authentication flow
3. Test each endpoint
4. Handle errors

---

## **✅ Ready to Start!**

Next: Create the schema files and first API endpoint!
