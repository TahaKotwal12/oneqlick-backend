# Coupons & Offers API Documentation

**Version:** 1.0  
**Base URL:** `/api/v1`  
**Date:** January 3, 2026

---

## Overview

The Coupons & Offers API provides endpoints for managing discount coupons and restaurant-specific offers in the OneQlick food delivery platform. Users can browse available coupons, validate them before checkout, and view their coupon usage history.

---

## Authentication

### Authentication Types

1. **Required** - Endpoints that require user authentication
   - Header: `Authorization: Bearer {access_token}`
   - Returns 401 if not authenticated

2. **Optional** - Endpoints that work for both authenticated and guest users
   - Header: `Authorization: Bearer {access_token}` (optional)
   - Returns personalized data if authenticated, generic data if not

3. **None** - Public endpoints (no authentication needed)

### Getting Access Token

To get an access token, use the `/api/v1/auth/login` endpoint:

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "user": {...},
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "...",
      "token_type": "bearer",
      "expires_in": 3600
    }
  }
}
```

---

## API Endpoints

### 1. Get Available Coupons

Get all available coupons that can be used.

**Endpoint:** `GET /api/v1/coupons`

**Authentication:** Optional

**Query Parameters:**
- `restaurant_id` (UUID, optional) - Filter by restaurant ID
- `min_order_amount` (Decimal, optional) - Filter by minimum order amount

**Request Example:**
```bash
GET /api/v1/coupons?min_order_amount=300
Authorization: Bearer {access_token}  # Optional
```

**Response:**
```json
{
  "coupons": [
    {
      "coupon_id": "123e4567-e89b-12d3-a456-426614174000",
      "code": "SAVE20",
      "title": "Save 20% on orders above ₹300",
      "description": "Get 20% discount on your order",
      "coupon_type": "percentage",
      "discount_value": 20.00,
      "min_order_amount": 300.00,
      "max_discount_amount": 100.00,
      "usage_limit": 1000,
      "used_count": 245,
      "valid_from": "2026-01-01T00:00:00Z",
      "valid_until": "2026-01-31T23:59:59Z",
      "is_active": true,
      "created_at": "2026-01-01T00:00:00Z",
      "is_expired": false,
      "is_available": true,
      "usage_remaining": 755
    }
  ],
  "total_count": 5,
  "available_count": 3
}
```

**Response Fields:**
- `coupons` - Array of coupon objects
- `total_count` - Total number of coupons
- `available_count` - Number of coupons user can actually use (excludes already used coupons for logged-in users)

**Coupon Types:**
- `percentage` - Percentage discount (e.g., 20% off)
- `fixed_amount` - Fixed amount discount (e.g., ₹50 off)
- `free_delivery` - Free delivery

**Status Codes:**
- `200 OK` - Success

---

### 2. Validate Coupon

Validate a coupon code and calculate discount.

**Endpoint:** `POST /api/v1/coupons/validate`

**Authentication:** Optional

**Request Body:**
```json
{
  "coupon_code": "SAVE20",
  "cart_total": 360.00,
  "restaurant_id": "123e4567-e89b-12d3-a456-426614174000"  // Optional
}
```

**Request Example:**
```bash
POST /api/v1/coupons/validate
Content-Type: application/json
Authorization: Bearer {access_token}  # Optional

{
  "coupon_code": "SAVE20",
  "cart_total": 360.00
}
```

**Success Response:**
```json
{
  "is_valid": true,
  "coupon": {
    "coupon_id": "123e4567-e89b-12d3-a456-426614174000",
    "code": "SAVE20",
    "title": "Save 20% on orders above ₹300",
    "description": "Get 20% discount on your order",
    "coupon_type": "percentage",
    "discount_value": 20.00,
    "min_order_amount": 300.00,
    "max_discount_amount": 100.00,
    "usage_limit": 1000,
    "used_count": 245,
    "valid_from": "2026-01-01T00:00:00Z",
    "valid_until": "2026-01-31T23:59:59Z",
    "is_active": true,
    "created_at": "2026-01-01T00:00:00Z",
    "is_expired": false,
    "is_available": true,
    "usage_remaining": 755
  },
  "discount_amount": 72.00,
  "final_amount": 288.00,
  "error_message": null
}
```

**Error Response (Invalid Coupon):**
```json
{
  "is_valid": false,
  "coupon": null,
  "discount_amount": 0.00,
  "final_amount": 360.00,
  "error_message": "Minimum order amount of ₹300 required"
}
```

**Validation Rules:**
1. Coupon must be active (`is_active = true`)
2. Current date must be between `valid_from` and `valid_until`
3. Cart total must be >= `min_order_amount`
4. Coupon must not have reached `usage_limit`
5. User must not have already used this coupon (for logged-in users)

**Possible Error Messages:**
- "Invalid coupon code"
- "This coupon is no longer active"
- "This coupon has expired"
- "This coupon is not yet valid"
- "Minimum order amount of ₹X required"
- "This coupon has reached its usage limit"
- "You have already used this coupon"

**Status Codes:**
- `200 OK` - Success (check `is_valid` field)

---

### 3. Get My Coupon Usage History

Get the current user's coupon usage history.

**Endpoint:** `GET /api/v1/coupons/my-usage`

**Authentication:** Required ✅

**Query Parameters:**
- `page` (int, default: 1) - Page number
- `page_size` (int, default: 20, max: 100) - Items per page

**Request Example:**
```bash
GET /api/v1/coupons/my-usage?page=1&page_size=20
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "usage_history": [
    {
      "user_coupon_usage_id": "123e4567-e89b-12d3-a456-426614174000",
      "coupon_code": "SAVE20",
      "coupon_title": "Save 20% on orders above ₹300",
      "order_id": "123e4567-e89b-12d3-a456-426614174001",
      "order_number": "OQ20260103001",
      "discount_amount": 72.00,
      "used_at": "2026-01-03T12:00:00Z"
    }
  ],
  "total_count": 5,
  "total_savings": 350.00
}
```

**Response Fields:**
- `usage_history` - Array of coupon usage records
- `total_count` - Total number of coupons used
- `total_savings` - Total amount saved using coupons

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Not authenticated

---

### 4. Get Active Offers

Get all active restaurant offers.

**Endpoint:** `GET /api/v1/coupons/offers`

**Authentication:** Optional

**Query Parameters:**
- `restaurant_id` (UUID, optional) - Filter by restaurant ID

**Request Example:**
```bash
GET /api/v1/coupons/offers
Authorization: Bearer {access_token}  # Optional
```

**Response:**
```json
{
  "offers": [
    {
      "offer_id": "123e4567-e89b-12d3-a456-426614174000",
      "restaurant_id": "123e4567-e89b-12d3-a456-426614174001",
      "title": "Free Delivery on orders above ₹200",
      "description": "Get free delivery",
      "discount_type": "free_delivery",
      "discount_value": 0.00,
      "min_order_amount": 200.00,
      "max_discount_amount": null,
      "valid_from": "2026-01-01T00:00:00Z",
      "valid_until": "2026-01-31T23:59:59Z",
      "is_active": true,
      "created_at": "2026-01-01T00:00:00Z",
      "is_expired": false
    }
  ],
  "total_count": 3
}
```

**Offer Types:**
- `percentage` - Percentage discount
- `fixed_amount` - Fixed amount discount
- `free_delivery` - Free delivery

**Status Codes:**
- `200 OK` - Success

---

### 5. Get Restaurant Offers

Get all active offers for a specific restaurant.

**Endpoint:** `GET /api/v1/coupons/restaurants/{restaurant_id}/offers`

**Authentication:** Optional

**Path Parameters:**
- `restaurant_id` (UUID, required) - Restaurant ID

**Request Example:**
```bash
GET /api/v1/coupons/restaurants/123e4567-e89b-12d3-a456-426614174001/offers
Authorization: Bearer {access_token}  # Optional
```

**Response:**
```json
{
  "offers": [
    {
      "offer_id": "123e4567-e89b-12d3-a456-426614174000",
      "restaurant_id": "123e4567-e89b-12d3-a456-426614174001",
      "title": "20% off on orders above ₹500",
      "description": "Special weekend offer",
      "discount_type": "percentage",
      "discount_value": 20.00,
      "min_order_amount": 500.00,
      "max_discount_amount": 150.00,
      "valid_from": "2026-01-01T00:00:00Z",
      "valid_until": "2026-01-31T23:59:59Z",
      "is_active": true,
      "created_at": "2026-01-01T00:00:00Z",
      "is_expired": false
    }
  ],
  "total_count": 2
}
```

**Status Codes:**
- `200 OK` - Success

---

## Usage Examples

### Example 1: Browse Available Coupons (Guest User)

```bash
curl -X GET "http://localhost:8001/api/v1/coupons?min_order_amount=300" \
  -H "Content-Type: application/json"
```

### Example 2: Validate Coupon Before Checkout (Logged-in User)

```bash
curl -X POST "http://localhost:8001/api/v1/coupons/validate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "coupon_code": "SAVE20",
    "cart_total": 360.00
  }'
```

### Example 3: Get Coupon Usage History

```bash
curl -X GET "http://localhost:8001/api/v1/coupons/my-usage?page=1&page_size=10" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Example 4: Get Restaurant Offers

```bash
curl -X GET "http://localhost:8001/api/v1/coupons/restaurants/123e4567-e89b-12d3-a456-426614174001/offers" \
  -H "Content-Type: application/json"
```

---

## Integration Flow

### Typical Checkout Flow with Coupons

1. **User adds items to cart**
   - Cart total: ₹360

2. **User browses available coupons**
   ```
   GET /api/v1/coupons?min_order_amount=360
   ```

3. **User selects a coupon and validates it**
   ```
   POST /api/v1/coupons/validate
   {
     "coupon_code": "SAVE20",
     "cart_total": 360.00
   }
   ```
   
   Response:
   ```json
   {
     "is_valid": true,
     "discount_amount": 72.00,
     "final_amount": 288.00
   }
   ```

4. **User proceeds to checkout with coupon applied**
   ```
   POST /api/v1/orders
   {
     "items": [...],
     "coupon_code": "SAVE20",
     "delivery_address_id": "...",
     ...
   }
   ```

5. **After order completion, coupon usage is recorded**
   - Entry created in `user_coupon_usage_tbl`
   - User can view in usage history

---

## Error Handling

### Common Error Responses

**400 Bad Request - Validation Error:**
```json
{
  "success": false,
  "error": "cart_total: ensure this value is greater than 0",
  "statusCode": 400
}
```

**401 Unauthorized - Not Authenticated:**
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found - Coupon Not Found:**
```json
{
  "is_valid": false,
  "error_message": "Invalid coupon code",
  "final_amount": 360.00
}
```

---

## Database Schema

### Coupons Table
```sql
CREATE TABLE core_mstr_one_qlick_coupons_tbl (
    coupon_id UUID PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    coupon_type coupon_type NOT NULL,  -- 'percentage', 'fixed_amount', 'free_delivery'
    discount_value DECIMAL(10, 2) NOT NULL,
    min_order_amount DECIMAL(10, 2) DEFAULT 0,
    max_discount_amount DECIMAL(10, 2),
    usage_limit INTEGER,
    used_count INTEGER DEFAULT 0,
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Coupon Usage Table
```sql
CREATE TABLE core_mstr_one_qlick_user_coupon_usage_tbl (
    user_coupon_usage_id UUID PRIMARY KEY,
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    coupon_id UUID REFERENCES core_mstr_one_qlick_coupons_tbl(coupon_id),
    order_id UUID REFERENCES core_mstr_one_qlick_orders_tbl(order_id),
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, coupon_id, order_id)
);
```

### Restaurant Offers Table
```sql
CREATE TABLE core_mstr_one_qlick_restaurant_offers_tbl (
    offer_id UUID PRIMARY KEY,
    restaurant_id UUID REFERENCES core_mstr_one_qlick_restaurants_tbl(restaurant_id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    discount_type VARCHAR(20) NOT NULL,  -- 'percentage', 'fixed_amount', 'free_delivery'
    discount_value DECIMAL(10, 2) NOT NULL,
    min_order_amount DECIMAL(10, 2),
    max_discount_amount DECIMAL(10, 2),
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Testing

### Test Scenarios

1. **Valid Coupon Application**
   - Create coupon with valid dates
   - Validate with cart total above minimum
   - Should return discount amount

2. **Expired Coupon**
   - Create coupon with past `valid_until`
   - Should return error: "This coupon has expired"

3. **Minimum Order Not Met**
   - Create coupon with min_order_amount = 300
   - Validate with cart_total = 200
   - Should return error: "Minimum order amount of ₹300 required"

4. **Already Used Coupon**
   - User uses coupon in order
   - Try to use same coupon again
   - Should return error: "You have already used this coupon"

5. **Usage Limit Reached**
   - Create coupon with usage_limit = 100, used_count = 100
   - Should return error: "This coupon has reached its usage limit"

---

## Notes

1. **Guest Users:** Can browse and validate coupons, but cannot view usage history
2. **Logged-in Users:** Get personalized coupon list (excludes already used coupons)
3. **Coupon Codes:** Case-insensitive (SAVE20 = save20 = SaVe20)
4. **One Use Per User:** Currently, each user can use a coupon only once
5. **Discount Calculation:**
   - Percentage: `(cart_total * discount_value) / 100`, capped at `max_discount_amount`
   - Fixed Amount: `discount_value`, cannot exceed cart total
   - Free Delivery: Applied to delivery fee (not cart total)

---

## Future Enhancements

1. **User-specific Coupons:** Coupons targeted to specific users
2. **First-time User Coupons:** Special coupons for new users
3. **Restaurant-specific Coupons:** Coupons valid only for certain restaurants
4. **Category-specific Coupons:** Coupons for specific food categories
5. **Stackable Coupons:** Allow multiple coupons on single order
6. **Referral Coupons:** Coupons generated from referral program
7. **Auto-apply Best Coupon:** Automatically apply best available coupon

---

**Document End**
