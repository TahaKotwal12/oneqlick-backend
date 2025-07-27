#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"
USER_ID=""

echo "🚀 Testing OneQlick User API Endpoints"
echo "========================================"

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

echo "Response: $RESPONSE" | jq .

USER_ID=$(echo $RESPONSE | jq -r '.data.user_id')
echo "Created user with ID: $USER_ID"

if [ "$USER_ID" == "null" ]; then
    echo "❌ Failed to create user"
    exit 1
fi

echo ""

# 2. Get user
echo "2. Getting user by ID..."
curl -s -X GET "$BASE_URL/users/$USER_ID" | jq .
echo ""

# 3. Update user
echo "3. Updating user..."
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Updated Test"
}' | jq .
echo ""

# 4. Verify email
echo "4. Verifying email..."
curl -s -X POST "$BASE_URL/users/$USER_ID/verify-email" | jq .
echo ""

# 5. Verify phone
echo "5. Verifying phone..."
curl -s -X POST "$BASE_URL/users/$USER_ID/verify-phone" | jq .
echo ""

# 6. Get all users
echo "6. Getting all users..."
curl -s -X GET "$BASE_URL/users?limit=5" | jq .
echo ""

# 7. Filter users by role
echo "7. Getting customers only..."
curl -s -X GET "$BASE_URL/users?role=customer&limit=3" | jq .
echo ""

echo "✅ Test completed successfully!"
echo ""
echo "To run this script:"
echo "1. Make sure your API server is running: uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo "2. Run: chmod +x api_docs/test_user_api.sh && ./api_docs/test_user_api.sh" 