# Restaurant API Documentation

This document describes the Restaurant API endpoints for the OneQlick Food Delivery System.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, the API doesn't require authentication. In production, JWT tokens should be implemented.

## Endpoints

### 1. Create Restaurant

**POST** `/restaurants`

Creates a new restaurant in the system.

**Validation Rules:**
- Owner must exist and have `restaurant_owner` role
- Owner must be active
- Phone number must be unique
- Email must be unique (if provided)

**Request Body:**
```json
{
  "owner_id": "uuid",
  "name": "Restaurant Name",
  "description": "Restaurant description",
  "phone": "+1234567890",
  "email": "restaurant@example.com",
  "address_line1": "123 Main Street",
  "address_line2": "Suite 100",
  "city": "New York",
  "state": "NY",
  "postal_code": "10001",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "image": "https://example.com/image.jpg",
  "cover_image": "https://example.com/cover.jpg",
  "cuisine_type": "Italian",
  "avg_delivery_time": 30,
  "min_order_amount": 15.00,
  "delivery_fee": 5.00,
  "opening_time": "09:00:00",
  "closing_time": "22:00:00"
}
```

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/restaurants" \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Restaurant Name",
    "description": "Restaurant description",
    "phone": "+1234567890",
    "email": "restaurant@example.com",
    "address_line1": "123 Main Street",
    "address_line2": "Suite 100",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "image": "https://example.com/image.jpg",
    "cover_image": "https://example.com/cover.jpg",
    "cuisine_type": "Italian",
    "avg_delivery_time": 30,
    "min_order_amount": 15.00,
    "delivery_fee": 5.00,
    "opening_time": "09:00:00",
    "closing_time": "22:00:00"
  }'
```

**Response (201 Created):**
```json
{
  "code": 201,
  "message": "Restaurant created successfully",
  "message_id": "0",
  "data": {
    "restaurant_id": "uuid",
    "owner_id": "uuid",
    "name": "Restaurant Name",
    "description": "Restaurant description",
    "phone": "+1234567890",
    "email": "restaurant@example.com",
    "address_line1": "123 Main Street",
    "address_line2": "Suite 100",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "latitude": "40.7128",
    "longitude": "-74.0060",
    "image": "https://example.com/image.jpg",
    "cover_image": "https://example.com/cover.jpg",
    "cuisine_type": "Italian",
    "avg_delivery_time": 30,
    "min_order_amount": "15.00",
    "delivery_fee": "5.00",
    "rating": "0.00",
    "total_ratings": 0,
    "status": "active",
    "is_open": true,
    "opening_time": "09:00:00",
    "closing_time": "22:00:00",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  }
}
```

### 2. Get Restaurant by ID

**GET** `/restaurants/{restaurant_id}`

Retrieves a specific restaurant by its UUID.

**cURL Command:**
```bash
curl -X GET "http://localhost:8000/api/v1/restaurants/550e8400-e29b-41d4-a716-446655440000"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Restaurant details retrieved successfully",
  "message_id": "0",
  "data": {
    "restaurant_id": "uuid",
    "owner_id": "uuid",
    "name": "Restaurant Name",
    "description": "Restaurant description",
    "phone": "+1234567890",
    "email": "restaurant@example.com",
    "address_line1": "123 Main Street",
    "address_line2": "Suite 100",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "latitude": "40.7128",
    "longitude": "-74.0060",
    "image": "https://example.com/image.jpg",
    "cover_image": "https://example.com/cover.jpg",
    "cuisine_type": "Italian",
    "avg_delivery_time": 30,
    "min_order_amount": "15.00",
    "delivery_fee": "5.00",
    "rating": "4.50",
    "total_ratings": 10,
    "status": "active",
    "is_open": true,
    "opening_time": "09:00:00",
    "closing_time": "22:00:00",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  }
}
```

### 3. Get All Restaurants

**GET** `/restaurants`

Retrieves a list of restaurants with optional filtering and pagination.
Returns empty list if no restaurants match the criteria.

**Query Parameters:**
- `skip` (optional): Number of restaurants to skip (default: 0)
- `limit` (optional): Maximum number of restaurants to return (default: 100, max: 1000)
- `status` (optional): Filter by restaurant status (active, inactive, suspended)
- `cuisine_type` (optional): Filter by cuisine type
- `city` (optional): Filter by city
- `is_open` (optional): Filter by open/closed status (true/false)

**Example Request:**
```
GET /restaurants?skip=0&limit=10&status=active&cuisine_type=Italian&city=New York&is_open=true
```

**cURL Command:**
```bash
curl -X GET "http://localhost:8000/api/v1/restaurants?skip=0&limit=10&status=active&cuisine_type=Italian&city=New%20York&is_open=true"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Retrieved 5 restaurants successfully",
  "message_id": "0",
  "data": [
    {
      "restaurant_id": "uuid",
      "name": "Restaurant Name",
      "description": "Restaurant description",
      "phone": "+1234567890",
      "city": "New York",
      "state": "NY",
      "cuisine_type": "Italian",
      "rating": "4.50",
      "total_ratings": 10,
      "status": "active",
      "is_open": true,
      "min_order_amount": "15.00",
      "delivery_fee": "5.00",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

**Empty Response (200 OK):**
```json
{
  "code": 200,
  "message": "No restaurants found matching the criteria",
  "message_id": "0",
  "data": []
}
```

### 4. Get Restaurants by Owner

**GET** `/restaurants/owner/{owner_id}`

Retrieves all restaurants owned by a specific user.
Returns empty list if owner not found or has no restaurants.

**cURL Command:**
```bash
curl -X GET "http://localhost:8000/api/v1/restaurants/owner/550e8400-e29b-41d4-a716-446655440000"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Retrieved 2 restaurants for owner successfully",
  "message_id": "0",
  "data": [
    {
      "restaurant_id": "uuid",
      "name": "Restaurant Name",
      "description": "Restaurant description",
      "phone": "+1234567890",
      "city": "New York",
      "state": "NY",
      "cuisine_type": "Italian",
      "rating": "4.50",
      "total_ratings": 10,
      "status": "active",
      "is_open": true,
      "min_order_amount": "15.00",
      "delivery_fee": "5.00",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

### 5. Search Restaurants by Location

**GET** `/restaurants/search/location`

Searches for restaurants within a specified radius of given coordinates.
Returns empty list if no restaurants found in the specified area.

**Query Parameters:**
- `latitude` (required): Latitude coordinate (-90 to 90)
- `longitude` (required): Longitude coordinate (-180 to 180)
- `radius_km` (optional): Search radius in kilometers (default: 10.0, min: 0.1, max: 100.0)

**Example Request:**
```
GET /restaurants/search/location?latitude=40.7128&longitude=-74.0060&radius_km=5.0
```

**cURL Command:**
```bash
curl -X GET "http://localhost:8000/api/v1/restaurants/search/location?latitude=40.7128&longitude=-74.0060&radius_km=5.0"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Found 3 restaurants within 5.0km",
  "message_id": "0",
  "data": [
    {
      "restaurant_id": "uuid",
      "name": "Restaurant Name",
      "description": "Restaurant description",
      "phone": "+1234567890",
      "city": "New York",
      "state": "NY",
      "cuisine_type": "Italian",
      "rating": "4.50",
      "total_ratings": 10,
      "status": "active",
      "is_open": true,
      "min_order_amount": "15.00",
      "delivery_fee": "5.00",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

### 6. Update Restaurant

**PUT** `/restaurants/{restaurant_id}`

Updates an existing restaurant's information.

**Request Body:**
```json
{
  "name": "Updated Restaurant Name",
  "description": "Updated description",
  "phone": "+1987654321",
  "email": "updated@restaurant.com",
  "address_line1": "456 New Street",
  "city": "Los Angeles",
  "state": "CA",
  "postal_code": "90210",
  "latitude": 34.0522,
  "longitude": -118.2437,
  "cuisine_type": "Mexican",
  "avg_delivery_time": 25,
  "min_order_amount": 20.00,
  "delivery_fee": 7.00,
  "status": "active",
  "is_open": true,
  "opening_time": "10:00:00",
  "closing_time": "23:00:00"
}
```

**cURL Command:**
```bash
curl -X PUT "http://localhost:8000/api/v1/restaurants/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Restaurant Name",
    "description": "Updated description",
    "phone": "+1987654321",
    "email": "updated@restaurant.com",
    "address_line1": "456 New Street",
    "city": "Los Angeles",
    "state": "CA",
    "postal_code": "90210",
    "latitude": 34.0522,
    "longitude": -118.2437,
    "cuisine_type": "Mexican",
    "avg_delivery_time": 25,
    "min_order_amount": 20.00,
    "delivery_fee": 7.00,
    "status": "active",
    "is_open": true,
    "opening_time": "10:00:00",
    "closing_time": "23:00:00"
  }'
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Restaurant updated successfully",
  "message_id": "0",
  "data": {
    "restaurant_id": "uuid",
    "owner_id": "uuid",
    "name": "Updated Restaurant Name",
    "description": "Updated description",
    "phone": "+1987654321",
    "email": "updated@restaurant.com",
    "address_line1": "456 New Street",
    "address_line2": null,
    "city": "Los Angeles",
    "state": "CA",
    "postal_code": "90210",
    "latitude": "34.0522",
    "longitude": "-118.2437",
    "image": null,
    "cover_image": null,
    "cuisine_type": "Mexican",
    "avg_delivery_time": 25,
    "min_order_amount": "20.00",
    "delivery_fee": "7.00",
    "rating": "4.50",
    "total_ratings": 10,
    "status": "active",
    "is_open": true,
    "opening_time": "10:00:00",
    "closing_time": "23:00:00",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T13:00:00"
  }
}
```

### 7. Delete Restaurant

**DELETE** `/restaurants/{restaurant_id}`

Performs a soft delete by setting the restaurant status to inactive.

**cURL Command:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/restaurants/550e8400-e29b-41d4-a716-446655440000"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Restaurant deleted successfully",
  "message_id": "0",
  "data": {
    "restaurant_id": "uuid",
    "deleted": true
  }
}
```

### 8. Toggle Restaurant Status

**POST** `/restaurants/{restaurant_id}/toggle-status`

Toggles the restaurant's open/closed status.

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/restaurants/550e8400-e29b-41d4-a716-446655440000/toggle-status"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Restaurant status toggled successfully",
  "message_id": "0",
  "data": {
    "restaurant_id": "uuid",
    "status_toggled": true
  }
}
```

### 9. Rate Restaurant

**POST** `/restaurants/{restaurant_id}/rate`

Adds a rating to the restaurant and updates the average rating.

**Query Parameters:**
- `rating` (required): Rating value between 1 and 5

**Example Request:**
```
POST /restaurants/{restaurant_id}/rate?rating=4.5
```

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/restaurants/550e8400-e29b-41d4-a716-446655440000/rate?rating=4.5"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Restaurant rated successfully",
  "message_id": "0",
  "data": {
    "restaurant_id": "uuid",
    "rating": 4.5,
    "rated": true
  }
}
```

### 10. Get Restaurant Statistics

**GET** `/restaurants/{restaurant_id}/statistics`

Retrieves statistics for a specific restaurant.

**cURL Command:**
```bash
curl -X GET "http://localhost:8000/api/v1/restaurants/550e8400-e29b-41d4-a716-446655440000/statistics"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "Restaurant statistics retrieved successfully",
  "message_id": "0",
  "data": {
    "restaurant_id": "uuid",
    "name": "Restaurant Name",
    "rating": 4.5,
    "total_ratings": 10,
    "status": "active",
    "is_open": true,
    "avg_delivery_time": 30,
    "min_order_amount": 15.0,
    "delivery_fee": 5.0
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "code": 400,
  "message": "Validation error message",
  "message_id": "0",
  "data": {}
}
```

**Common Validation Errors:**
- `"Owner user not found"` - When the provided owner_id doesn't exist
- `"User must have restaurant_owner role to create a restaurant"` - When user doesn't have the required role
- `"Owner user must be active to create a restaurant"` - When owner is inactive
- `"Restaurant with this phone number already exists"` - When phone number is already in use
- `"Restaurant with this email already exists"` - When email is already in use

### 404 Not Found
```json
{
  "code": 404,
  "message": "Restaurant not found",
  "message_id": "0",
  "data": {}
}
```

### 500 Internal Server Error
```json
{
  "code": 500,
  "message": "An error occurred while processing the request",
  "message_id": "0",
  "data": {}
}
```

## Data Types

### Restaurant Status Enum
- `active`: Restaurant is active and can receive orders
- `inactive`: Restaurant is inactive (soft deleted)
- `suspended`: Restaurant is temporarily suspended

### Validation Rules
- `name`: Required, 1-255 characters
- `phone`: Required, 10-20 characters, must be unique
- `email`: Optional, must be valid email format, must be unique if provided
- `latitude`: Required, between -90 and 90
- `longitude`: Required, between -180 and 180
- `avg_delivery_time`: Optional, must be positive integer
- `min_order_amount`: Optional, must be non-negative decimal
- `delivery_fee`: Optional, must be non-negative decimal
- `rating`: Must be between 1 and 5

## Testing

Use the provided test script to verify all endpoints:

```bash
chmod +x api_docs/test_restaurant_api.sh
./api_docs/test_restaurant_api.sh
```

Make sure the FastAPI server is running on `localhost:8000` before running the test script. 