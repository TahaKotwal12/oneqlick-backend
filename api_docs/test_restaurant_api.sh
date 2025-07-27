#!/bin/bash

# Test script for Restaurant API endpoints
# Make sure the FastAPI server is running on localhost:8000

BASE_URL="http://localhost:8000/api/v1"
echo "Testing Restaurant API endpoints..."
echo "=================================="

# First, let's create a test user (restaurant owner)
echo "1. Creating a test user (restaurant owner)..."
USER_RESPONSE=$(curl -s -X POST "${BASE_URL}/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "restaurant.owner@test.com",
    "phone": "+1234567890",
    "password": "testpassword123",
    "first_name": "John",
    "last_name": "RestaurantOwner",
    "role": "restaurant_owner"
  }')

echo "User Response: $USER_RESPONSE"
USER_ID=$(echo $USER_RESPONSE | grep -o '"user_id":"[^"]*"' | cut -d'"' -f4)
echo "Created User ID: $USER_ID"

if [ -z "$USER_ID" ]; then
    echo "Failed to create user. Exiting."
    exit 1
fi

# Test owner validation - try to create restaurant with non-restaurant_owner user
echo -e "\n1.5. Testing owner validation (should fail)..."
curl -s -X POST "${BASE_URL}/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@test.com",
    "phone": "+1111111111",
    "password": "testpassword123",
    "first_name": "Jane",
    "last_name": "Customer",
    "role": "customer"
  }' > /dev/null

CUSTOMER_RESPONSE=$(curl -s -X POST "${BASE_URL}/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer2@test.com",
    "phone": "+1111111112",
    "password": "testpassword123",
    "first_name": "Jane",
    "last_name": "Customer",
    "role": "customer"
  }')

CUSTOMER_ID=$(echo $CUSTOMER_RESPONSE | grep -o '"user_id":"[^"]*"' | cut -d'"' -f4)

echo "Testing restaurant creation with customer role (should fail):"
curl -s -X POST "${BASE_URL}/restaurants" \
  -H "Content-Type: application/json" \
  -d "{
    \"owner_id\": \"$CUSTOMER_ID\",
    \"name\": \"Invalid Restaurant\",
    \"phone\": \"+9999999999\",
    \"address_line1\": \"123 Test Street\",
    \"city\": \"Test City\",
    \"state\": \"Test State\",
    \"postal_code\": \"12345\",
    \"latitude\": 40.7128,
    \"longitude\": -74.0060
  }" | jq '.'

# 2. Create a restaurant
echo -e "\n2. Creating a restaurant..."
RESTAURANT_RESPONSE=$(curl -s -X POST "${BASE_URL}/restaurants" \
  -H "Content-Type: application/json" \
  -d "{
    \"owner_id\": \"$USER_ID\",
    \"name\": \"Test Restaurant\",
    \"description\": \"A delicious test restaurant\",
    \"phone\": \"+1987654321\",
    \"email\": \"test@restaurant.com\",
    \"address_line1\": \"123 Test Street\",
    \"city\": \"Test City\",
    \"state\": \"Test State\",
    \"postal_code\": \"12345\",
    \"latitude\": 40.7128,
    \"longitude\": -74.0060,
    \"cuisine_type\": \"Italian\",
    \"avg_delivery_time\": 30,
    \"min_order_amount\": 15.00,
    \"delivery_fee\": 5.00
  }")

echo "Restaurant Response: $RESTAURANT_RESPONSE"
RESTAURANT_ID=$(echo $RESTAURANT_RESPONSE | grep -o '"restaurant_id":"[^"]*"' | cut -d'"' -f4)
echo "Created Restaurant ID: $RESTAURANT_ID"

if [ -z "$RESTAURANT_ID" ]; then
    echo "Failed to create restaurant. Exiting."
    exit 1
fi

# 3. Get restaurant by ID
echo -e "\n3. Getting restaurant by ID..."
curl -s -X GET "${BASE_URL}/restaurants/${RESTAURANT_ID}" | jq '.'

# 4. Get all restaurants
echo -e "\n4. Getting all restaurants..."
curl -s -X GET "${BASE_URL}/restaurants" | jq '.'

# 5. Get restaurants by owner
echo -e "\n5. Getting restaurants by owner..."
curl -s -X GET "${BASE_URL}/restaurants/owner/${USER_ID}" | jq '.'

# 6. Search restaurants by location
echo -e "\n6. Searching restaurants by location..."
curl -s -X GET "${BASE_URL}/restaurants/search/location?latitude=40.7128&longitude=-74.0060&radius_km=10" | jq '.'

# 7. Update restaurant
echo -e "\n7. Updating restaurant..."
curl -s -X PUT "${BASE_URL}/restaurants/${RESTAURANT_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Test Restaurant",
    "description": "An updated delicious test restaurant",
    "cuisine_type": "Mexican",
    "avg_delivery_time": 25
  }' | jq '.'

# 8. Rate restaurant
echo -e "\n8. Rating restaurant..."
curl -s -X POST "${BASE_URL}/restaurants/${RESTAURANT_ID}/rate?rating=4.5" | jq '.'

# 9. Get restaurant statistics
echo -e "\n9. Getting restaurant statistics..."
curl -s -X GET "${BASE_URL}/restaurants/${RESTAURANT_ID}/statistics" | jq '.'

# 10. Toggle restaurant status
echo -e "\n10. Toggling restaurant status..."
curl -s -X POST "${BASE_URL}/restaurants/${RESTAURANT_ID}/toggle-status" | jq '.'

# 11. Get restaurant again to see changes
echo -e "\n11. Getting updated restaurant..."
curl -s -X GET "${BASE_URL}/restaurants/${RESTAURANT_ID}" | jq '.'

# 12. Delete restaurant (soft delete)
echo -e "\n12. Deleting restaurant..."
curl -s -X DELETE "${BASE_URL}/restaurants/${RESTAURANT_ID}" | jq '.'

# 13. Verify restaurant is deleted (should return 404)
echo -e "\n13. Verifying restaurant is deleted..."
curl -s -X GET "${BASE_URL}/restaurants/${RESTAURANT_ID}" | jq '.'

echo -e "\n=================================="
echo "Restaurant API testing completed!" 