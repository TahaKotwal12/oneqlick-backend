# OTP Setup Guide

This guide will help you set up OTP (One-Time Password) verification for your OneQlick Food Delivery application.

## Prerequisites

- Python 3.8+
- Redis server
- Twilio account (for production SMS)

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Redis Setup

### Option A: Local Redis Installation

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### macOS
```bash
brew install redis
brew services start redis
```

#### Windows
Download Redis from [https://redis.io/download](https://redis.io/download) or use WSL.

### Option B: Docker Redis
```bash
docker run -d --name redis -p 6379:6379 redis:alpine
```

### Option C: Cloud Redis (Recommended for Production)
- **Redis Cloud**: [https://redis.com/try-free/](https://redis.com/try-free/)
- **AWS ElastiCache**: [https://aws.amazon.com/elasticache/](https://aws.amazon.com/elasticache/)
- **Google Cloud Memorystore**: [https://cloud.google.com/memorystore](https://cloud.google.com/memorystore)

### Test Redis Connection
```bash
redis-cli ping
# Should return: PONG
```

## 3. Environment Configuration

Create or update your `.env` file:

```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_redis_password  # Optional

# SMS Configuration
USE_MOCK_SMS=true  # Set to false for production

# Twilio Configuration (for production)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

## 4. Twilio Setup (Production)

### Step 1: Create Twilio Account
1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. Verify your email and phone number

### Step 2: Get Credentials
1. Go to [Twilio Console](https://console.twilio.com/)
2. Find your **Account SID** and **Auth Token**
3. Copy these to your `.env` file

### Step 3: Get a Phone Number
1. In Twilio Console, go to **Phone Numbers** → **Manage** → **Active numbers**
2. Click **Get a trial number**
3. Choose a number and copy it to `TWILIO_PHONE_NUMBER`

### Step 4: Verify Your Phone (Free Trial)
For free trial accounts, you need to verify recipient phone numbers:
1. Go to **Phone Numbers** → **Manage** → **Verified Caller IDs**
2. Add your phone number for testing

## 5. Development vs Production Setup

### Development Setup
```bash
# Use mock SMS (OTPs printed to console)
USE_MOCK_SMS=true

# Local Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Production Setup
```bash
# Use Twilio for real SMS
USE_MOCK_SMS=false
TWILIO_ACCOUNT_SID=UScedd67287f64af903baf413d5abb84d8
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Cloud Redis
REDIS_HOST=your-redis-host.com
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
```

## 6. Testing the Setup

### Start the Application
```bash
uvicorn app.main:app --reload
```

### Test OTP Functionality
```bash
# Make the test script executable
chmod +x api_docs/test_otp_api.sh

# Run the test
./api_docs/test_otp_api.sh
```

### Manual Testing
```bash
# 1. Request OTP
curl -X POST "http://localhost:8000/api/v1/otp/request" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'

# 2. Check console for OTP (in development mode)
# Look for: "📱 MOCK SMS SENT" message

# 3. Verify OTP
curl -X POST "http://localhost:8000/api/v1/otp/verify" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890", "otp": "123456"}'
```

## 7. Integration with Frontend

### React Native Example
```javascript
// Request OTP
const requestOTP = async (phone) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/otp/request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phone }),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error requesting OTP:', error);
  }
};

// Verify OTP
const verifyOTP = async (phone, otp) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/otp/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phone, otp }),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error verifying OTP:', error);
  }
};
```

## 8. Security Best Practices

### Rate Limiting
- OTP requests are limited to 1 per minute per phone number
- Maximum 3 verification attempts per OTP
- OTPs expire after 5 minutes

### Phone Number Validation
- Validates phone number format
- Strips special characters
- Supports international formats

### Secure Storage
- OTPs stored in Redis with automatic expiry
- No OTPs stored in database
- Automatic cleanup after verification

## 9. Troubleshooting

### Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# Check Redis logs
sudo journalctl -u redis-server

# Test connection from Python
python -c "import redis; r = redis.Redis(); print(r.ping())"
```

### Twilio Issues
1. **Invalid Phone Number**: Ensure phone number is in E.164 format (+1234567890)
2. **Unauthorized**: Check Account SID and Auth Token
3. **Insufficient Credits**: Add funds to your Twilio account
4. **Unverified Number**: For free trial, verify recipient phone numbers

### Common Error Messages
- `"Redis connection error"`: Check Redis server status
- `"Twilio client not initialized"`: Check Twilio credentials
- `"Please wait X seconds"`: Rate limiting in effect
- `"OTP expired"`: Request a new OTP

## 10. Monitoring and Logs

### Enable Debug Logging
```python
import logging
logging.getLogger('app.domain.services.otp_service').setLevel(logging.DEBUG)
logging.getLogger('app.domain.services.sms_service').setLevel(logging.DEBUG)
```

### Monitor OTP Usage
```bash
# Check Redis keys
redis-cli keys "otp:*"

# Check rate limiting
redis-cli keys "otp_request:*"
```

## 11. Production Deployment

### Environment Variables
```bash
# Production environment
export USE_MOCK_SMS=false
export TWILIO_ACCOUNT_SID=your_production_sid
export TWILIO_AUTH_TOKEN=your_production_token
export TWILIO_PHONE_NUMBER=your_production_number
export REDIS_HOST=your_production_redis_host
export REDIS_PASSWORD=your_production_redis_password
```

### Health Checks
```bash
# Check Redis connection
curl http://localhost:8000/health

# Check OTP service
curl -X POST "http://localhost:8000/api/v1/otp/request" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

## 12. Cost Considerations

### Twilio Pricing (as of 2024)
- **Free Trial**: $15-20 credit included
- **SMS**: ~$0.0079 per message (US)
- **International**: Varies by country

### Redis Pricing
- **Local**: Free
- **Redis Cloud**: Free tier available
- **AWS ElastiCache**: Pay per use

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check application logs
4. Verify environment configuration 