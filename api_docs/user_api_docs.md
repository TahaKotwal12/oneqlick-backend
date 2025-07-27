# OneQlick User API Documentation

This document contains all the API endpoints for user management in the OneQlick food delivery system.

**Base URL:** `http://localhost:8000/api/v1`

## Headers
All POST/PUT requests require:
```bash
-H "Content-Type: application/json"
```

---

## 1. Create User

**Endpoint:** `POST /users`  
**Description:** Create a new user in the system

### Request Body
```json
{
  "email": "john.doe@example.com",
  "phone": "+919876543210",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "customer",
  "profile_image": "https://example.com/profile.jpg"
}
```

### User Roles
- `customer` - End user who orders food
- `admin` - System administrator
- `delivery_partner` - Delivery person
- `restaurant_owner` - Restaurant owner/manager

### Curl Example
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "phone": "+919876543210",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "customer",
  "profile_image": "https://example.com/profile.jpg"
}'
```

### Response (201 Created)
```json
{
  "code": 201,
  "message": "User created successfully",
  "message_id": "0",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "john.doe@example.com",
    "phone": "+919876543210",
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer",
    "status": "active",
    "profile_image": "https://example.com/profile.jpg",
    "email_verified": false,
    "phone_verified": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

## 2. Get User by ID

**Endpoint:** `GET /users/{user_id}`  
**Description:** Retrieve user details by UUID

### Curl Example
```bash
curl -X GET "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000"
```

### Response (200 OK)
```json
{
  "code": 200,
  "message": "User details retrieved successfully",
  "message_id": "0",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "john.doe@example.com",
    "phone": "+919876543210",
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer",
    "status": "active",
    "profile_image": "https://example.com/profile.jpg",
    "email_verified": false,
    "phone_verified": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

## 3. Get All Users

**Endpoint:** `GET /users`  
**Description:** Get list of users with pagination and filtering

### Query Parameters
- `skip` (optional): Number of users to skip (default: 0)
- `limit` (optional): Maximum number of users to return (default: 100, max: 1000)
- `role` (optional): Filter by user role (`customer`, `admin`, `delivery_partner`, `restaurant_owner`)
- `status` (optional): Filter by user status (`active`, `inactive`, `suspended`)

### Curl Examples

**Get all users (paginated):**
```bash
curl -X GET "http://localhost:8000/api/v1/users?skip=0&limit=10"
```

**Filter by role:**
```bash
curl -X GET "http://localhost:8000/api/v1/users?role=customer&limit=20"
```

**Filter by status:**
```bash
curl -X GET "http://localhost:8000/api/v1/users?status=active&skip=10&limit=10"
```

### Response (200 OK)
```json
{
  "code": 200,
  "message": "Retrieved 2 users successfully",
  "message_id": "0",
  "data": [
    {
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "customer",
      "status": "active",
      "email_verified": false,
      "phone_verified": false,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "user_id": "456e7890-e89b-12d3-a456-426614174001",
      "email": "jane.smith@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "role": "delivery_partner",
      "status": "active",
      "email_verified": true,
      "phone_verified": true,
      "created_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

---

## 4. Update User

**Endpoint:** `PUT /users/{user_id}`  
**Description:** Update user information (partial update)

### Request Body (All fields optional)
```json
{
  "first_name": "Johnny",
  "last_name": "Doe",
  "phone": "+919876543211",
  "profile_image": "https://example.com/new-profile.jpg",
  "status": "active"
}
```

### Curl Example
```bash
curl -X PUT "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Johnny",
  "phone": "+919876543211",
  "profile_image": "https://example.com/new-profile.jpg"
}'
```

### Response (200 OK)
```json
{
  "code": 200,
  "message": "User updated successfully",
  "message_id": "0",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "john.doe@example.com",
    "phone": "+919876543211",
    "first_name": "Johnny",
    "last_name": "Doe",
    "role": "customer",
    "status": "active",
    "profile_image": "https://example.com/new-profile.jpg",
    "email_verified": false,
    "phone_verified": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

---

## 5. Delete User

**Endpoint:** `DELETE /users/{user_id}`  
**Description:** Soft delete a user (sets status to inactive)

### Curl Example
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000"
```

### Response (200 OK)
```json
{
  "code": 200,
  "message": "User deleted successfully",
  "message_id": "0",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "deleted": true
  }
}
```

---

## 6. Verify User Email

**Endpoint:** `POST /users/{user_id}/verify-email`  
**Description:** Mark user email as verified

### Curl Example
```bash
curl -X POST "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000/verify-email"
```

### Response (200 OK)
```json
{
  "code": 200,
  "message": "Email verified successfully",
  "message_id": "0",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "email_verified": true
  }
}
```

---

## 7. Verify User Phone

**Endpoint:** `POST /users/{user_id}/verify-phone`  
**Description:** Mark user phone as verified

### Curl Example
```bash
curl -X POST "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000/verify-phone"
```

### Response (200 OK)
```json
{
  "code": 200,
  "message": "Phone verified successfully",
  "message_id": "0",
  "data": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "phone_verified": true
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email or phone already exists"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "first_name"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "An error occurred while creating the user"
}
```

---

## Testing Script

Create a test script to verify all endpoints:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"
USER_ID=""

# 1. Create user
echo "1. Creating user..."
RESPONSE=$(curl -s -X POST "$BASE_URL/users" \
-H "Content-Type: application/json" \
-d '{
  "email": "test.user@oneqlick.com",
  "phone": "+919999999999",
  "password": "testpassword123",
  "first_name": "Test",
  "last_name": "User",
  "role": "customer"
}')

USER_ID=$(echo $RESPONSE | jq -r '.data.user_id')
echo "Created user with ID: $USER_ID"

# 2. Get user
echo "2. Getting user..."
curl -s -X GET "$BASE_URL/users/$USER_ID" | jq

# 3. Update user
echo "3. Updating user..."
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Updated Test"
}' | jq

# 4. Verify email
echo "4. Verifying email..."
curl -s -X POST "$BASE_URL/users/$USER_ID/verify-email" | jq

# 5. Get all users
echo "5. Getting all users..."
curl -s -X GET "$BASE_URL/users?limit=5" | jq

echo "Test completed!"
```

Save this as `test_user_api.sh` and run with `chmod +x test_user_api.sh && ./test_user_api.sh` 