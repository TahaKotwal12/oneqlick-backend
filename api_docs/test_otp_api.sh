#!/bin/bash

# Test script for OTP API endpoints
# Make sure the FastAPI server is running on localhost:8000

BASE_URL="http://localhost:8000/api/v1"
echo "Testing OTP API endpoints..."
echo "=================================="

# Test phone number
PHONE_NUMBER="+1234567890"

# 1. Request OTP
echo "1. Requesting OTP..."
OTP_RESPONSE=$(curl -s -X POST "${BASE_URL}/otp/request" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"${PHONE_NUMBER}\"
  }")

echo "OTP Response: $OTP_RESPONSE"

# Extract OTP from console output (for mock SMS)
echo -e "\n📱 Check the console output above for the OTP code!"
echo -e "📱 Or check the logs for the OTP message.\n"

# Wait for user to input OTP
read -p "Enter the OTP code from the console/logs: " OTP_CODE

if [ -z "$OTP_CODE" ]; then
    echo "No OTP code entered. Exiting."
    exit 1
fi

# 2. Verify OTP
echo -e "\n2. Verifying OTP..."
VERIFY_RESPONSE=$(curl -s -X POST "${BASE_URL}/otp/verify" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"${PHONE_NUMBER}\",
    \"otp\": \"${OTP_CODE}\"
  }")

echo "Verify Response: $VERIFY_RESPONSE"

# 3. Test rate limiting
echo -e "\n3. Testing rate limiting (should fail)..."
RATE_LIMIT_RESPONSE=$(curl -s -X POST "${BASE_URL}/otp/request" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"${PHONE_NUMBER}\"
  }")

echo "Rate Limit Response: $RATE_LIMIT_RESPONSE"

# 4. Test invalid OTP
echo -e "\n4. Testing invalid OTP (should fail)..."
INVALID_OTP_RESPONSE=$(curl -s -X POST "${BASE_URL}/otp/verify" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"${PHONE_NUMBER}\",
    \"otp\": \"000000\"
  }")

echo "Invalid OTP Response: $INVALID_OTP_RESPONSE"

# 5. Test invalid phone number
echo -e "\n5. Testing invalid phone number (should fail)..."
INVALID_PHONE_RESPONSE=$(curl -s -X POST "${BASE_URL}/otp/request" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"123\"
  }")

echo "Invalid Phone Response: $INVALID_PHONE_RESPONSE"

# 6. Test with user verification (if you have a user)
echo -e "\n6. Testing OTP verification for specific user..."
echo "Note: This requires a valid user ID. You can create a user first and use their ID."

# Example with a sample user ID (replace with actual user ID)
# USER_ID="550e8400-e29b-41d4-a716-446655440000"
# USER_VERIFY_RESPONSE=$(curl -s -X POST "${BASE_URL}/otp/verify-user/${USER_ID}" \
#   -H "Content-Type: application/json" \
#   -d "{
#     \"phone\": \"${PHONE_NUMBER}\",
#     \"otp\": \"${OTP_CODE}\"
#   }")
# echo "User Verify Response: $USER_VERIFY_RESPONSE"

echo -e "\n=================================="
echo "OTP API testing completed!"
echo -e "\n📝 Notes:"
echo "- In development mode, OTPs are printed to console/logs"
echo "- For production, set USE_MOCK_SMS=false and configure Twilio credentials"
echo "- Rate limiting: 1 request per minute per phone number"
echo "- OTP expires after 5 minutes"
echo "- Maximum 3 verification attempts per OTP" 