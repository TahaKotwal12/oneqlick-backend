# OTP Verification API Documentation

This document describes the OTP (One-Time Password) verification API endpoints for the OneQlick Food Delivery System.

## Base URL
```
http://localhost:8000/api/v1
```

## Overview

The OTP system provides phone number verification functionality with the following features:

- **6-digit OTP generation** with 5-minute expiry
- **Rate limiting**: 1 request per minute per phone number
- **Maximum 3 verification attempts** per OTP
- **Automatic user phone verification** when OTP is valid
- **Mock SMS support** for development/testing
- **Twilio integration** for production SMS

## Environment Variables

### Development (Mock SMS)
```bash
USE_MOCK_SMS=true
```

### Production (Twilio)
```bash
USE_MOCK_SMS=false
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

### Redis Configuration
```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_redis_password  # Optional
```

## Endpoints

### 1. Request OTP

**POST** `/otp/request`

Sends an OTP to the specified phone number for verification.

**Request Body:**
```json
{
  "phone": "+1234567890"
}
```

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/otp/request" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890"
  }'
```

**Response (200 OK):**
```json
{
  "code": 200,
  "message": "OTP sent successfully",
  "message_id": "0",
  "data": {
    "success": true,
    "message": "OTP sent successfully",
    "phone": "+1234567890",
    "expires_in_minutes": 5,
    "attempts_remaining": 3
  }
}
```

**Response (429 Too Many Requests):**
```json
{
  "code": 429,
  "message": "Please wait 45 seconds before requesting another OTP",
  "message_id": "0",
  "data": {}
}
```

### 2. Verify OTP

**POST** `/otp/verify`

Verifies the OTP sent to the phone number. Automatically marks user's phone as verified if user exists.

**Request Body:**
```json
{
  "phone": "+1234567890",
  "otp": "123456"
}
```

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/otp/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890",
    "otp": "123456"
  }'
```

**Response (200 OK) - Success:**
```json
{
  "code": 200,
  "message": "OTP verified successfully",
  "message_id": "0",
  "data": {
    "success": true,
    "message": "OTP verified successfully",
    "phone": "+1234567890",
    "verified": true
  }
}
```

**Response (200 OK) - Failure:**
```json
{
  "code": 200,
  "message": "Invalid OTP. 2 attempts remaining",
  "message_id": "0",
  "data": {
    "success": false,
    "message": "Invalid OTP. 2 attempts remaining",
    "phone": "+1234567890",
    "verified": false
  }
}
```

### 3. Verify OTP for Specific User

**POST** `/otp/verify-user/{user_id}`

Verifies the OTP and marks the specific user's phone as verified.

**Request Body:**
```json
{
  "phone": "+1234567890",
  "otp": "123456"
}
```

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/otp/verify-user/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1234567890",
    "otp": "123456"
  }'
```

**Response (200 OK) - Success:**
```json
{
  "code": 200,
  "message": "OTP verified successfully",
  "message_id": "0",
  "data": {
    "success": true,
    "message": "OTP verified successfully",
    "phone": "+1234567890",
    "verified": true
  }
}
```

**Response (404 Not Found):**
```json
{
  "code": 404,
  "message": "User not found",
  "message_id": "0",
  "data": {}
}
```

**Response (400 Bad Request):**
```json
{
  "code": 400,
  "message": "Phone number does not match user's phone",
  "message_id": "0",
  "data": {}
}
```

## Error Responses

### 400 Bad Request
```json
{
  "code": 400,
  "message": "Invalid phone number format",
  "message_id": "0",
  "data": {}
}
```

### 429 Too Many Requests
```json
{
  "code": 429,
  "message": "Please wait 30 seconds before requesting another OTP",
  "message_id": "0",
  "data": {}
}
```

### 500 Internal Server Error
```json
{
  "code": 500,
  "message": "Failed to send SMS: Twilio SMS error",
  "message_id": "0",
  "data": {}
}
```

## Validation Rules

### Phone Number
- Must be between 7 and 15 digits
- Can include country code (e.g., +1)
- Special characters are stripped for validation

### OTP
- Must be 4-8 digits only
- Generated as 6-digit code by default
- Case-insensitive

## Rate Limiting

- **OTP Requests**: 1 request per minute per phone number
- **Verification Attempts**: Maximum 3 attempts per OTP
- **OTP Expiry**: 5 minutes from generation

## Development vs Production

### Development Mode (Mock SMS)
- OTPs are printed to console/logs
- No actual SMS sent
- Perfect for testing and development
- Set `USE_MOCK_SMS=true`

### Production Mode (Twilio)
- Real SMS sent via Twilio
- Requires Twilio account and credentials
- Set `USE_MOCK_SMS=false`

## Testing

### Using the Test Script
```bash
chmod +x api_docs/test_otp_api.sh
./api_docs/test_otp_api.sh
```

### Manual Testing
1. **Request OTP**: Send POST to `/otp/request`
2. **Check Console/Logs**: Find the OTP in the output
3. **Verify OTP**: Send POST to `/otp/verify` with the OTP
4. **Test Rate Limiting**: Try requesting OTP again immediately

### Example Flow
```bash
# 1. Request OTP
curl -X POST "http://localhost:8000/api/v1/otp/request" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'

# 2. Check console for OTP (e.g., "123456")

# 3. Verify OTP
curl -X POST "http://localhost:8000/api/v1/otp/verify" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890", "otp": "123456"}'
```

## Integration with User System

When an OTP is successfully verified:
1. If a user exists with that phone number, their `phone_verified` field is set to `true`
2. The OTP is deleted from Redis
3. A success response is returned

## Security Features

- **OTP Expiry**: Automatic cleanup after 5 minutes
- **Rate Limiting**: Prevents abuse
- **Attempt Limiting**: Prevents brute force attacks
- **Secure Storage**: OTPs stored in Redis with expiry
- **Phone Validation**: Ensures valid phone number format

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Ensure Redis is running
   - Check Redis configuration in environment variables

2. **Twilio SMS Failures**
   - Verify Twilio credentials
   - Check phone number format
   - Ensure sufficient Twilio credits

3. **Rate Limiting**
   - Wait 60 seconds between OTP requests
   - Check Redis for rate limiting data

4. **OTP Expiry**
   - OTPs expire after 5 minutes
   - Request a new OTP if expired

### Debug Mode
Enable debug logging to see detailed OTP operations:
```python
import logging
logging.getLogger('app.domain.services.otp_service').setLevel(logging.DEBUG)
``` 