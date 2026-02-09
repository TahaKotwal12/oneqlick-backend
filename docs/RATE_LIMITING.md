# Rate Limiting - OneQlick Backend

## Overview

The OneQlick backend implements comprehensive rate limiting to protect against abuse, brute force attacks, and ensure fair usage across all API endpoints.

## Features

✅ **Multi-tier rate limiting** - Different limits for different endpoint types  
✅ **Dual storage backends** - Redis for production, in-memory for development  
✅ **Sliding window algorithm** - Accurate rate limiting without burst allowances  
✅ **IP and user-based limiting** - Flexible identification strategies  
✅ **Rate limit headers** - Standard HTTP headers for client awareness  
✅ **Whitelist support** - Bypass rate limits for trusted IPs  
✅ **Global protection** - DDoS prevention with global rate limiter

## Rate Limit Tiers

| Endpoint Type | Limit | Window | Identifier |
|--------------|-------|--------|------------|
| **Global** | 1000 req | 1 hour | IP Address |
| **Authentication** | | | |
| - Login | 10 req | 1 minute | IP Address |
| - Signup | 5 req | 1 minute | IP Address |
| - OTP Send | 5 req | 1 minute | IP Address |
| - Password Reset | 3 req | 1 minute | IP Address |
| **Public Endpoints** | 100 req | 1 minute | IP Address |
| **Search** | 50 req | 1 minute | IP Address |
| **Authenticated Users** | 200 req | 1 minute | User ID |
| **Admin Users** | 500 req | 1 minute | User ID |
| **Partner Users** | 300 req | 1 minute | User ID |

## Configuration

All rate limits can be configured via environment variables:

```env
# Enable/disable rate limiting
RATE_LIMIT_ENABLED=true

# Storage backend: "redis" or "memory"
RATE_LIMIT_STORAGE=redis

# Global limits
RATE_LIMIT_GLOBAL_PER_HOUR=1000

# Authentication endpoints
RATE_LIMIT_AUTH_LOGIN_PER_MINUTE=10
RATE_LIMIT_AUTH_SIGNUP_PER_MINUTE=5
RATE_LIMIT_AUTH_OTP_PER_MINUTE=5
RATE_LIMIT_AUTH_PASSWORD_RESET_PER_MINUTE=3

# Public endpoints
RATE_LIMIT_PUBLIC_PER_MINUTE=100

# Search endpoints
RATE_LIMIT_SEARCH_PER_MINUTE=50

# Authenticated endpoints
RATE_LIMIT_USER_PER_MINUTE=200
RATE_LIMIT_ADMIN_PER_MINUTE=500
RATE_LIMIT_PARTNER_PER_MINUTE=300

# Whitelist (comma-separated IPs)
RATE_LIMIT_WHITELIST=127.0.0.1,::1
```

## Response Headers

All responses include rate limit headers:

```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1704729600
```

- **X-RateLimit-Limit**: Maximum requests allowed in the window
- **X-RateLimit-Remaining**: Requests remaining in current window
- **X-RateLimit-Reset**: Unix timestamp when the limit resets

## Rate Limit Exceeded Response

When rate limit is exceeded, the API returns HTTP 429:

```json
{
  "code": 429,
  "message": "Rate limit exceeded. Try again in 45 seconds.",
  "message_id": "RATE_LIMIT_EXCEEDED",
  "data": {
    "limit": 10,
    "window": 60,
    "reset_time": 1704729600
  }
}
```

## Usage in Code

### Using Decorators

```python
from app.utils.rate_limiter import rate_limit, rate_limit_auth, rate_limit_public

# Custom rate limit
@router.post("/custom-endpoint")
@rate_limit(limit=20, window=60)
async def custom_endpoint():
    pass

# Authentication rate limit (10 req/min)
@router.post("/login")
@rate_limit_auth()
async def login():
    pass

# Public rate limit (100 req/min)
@router.get("/restaurants")
@rate_limit_public()
async def get_restaurants():
    pass

# User-based rate limit (uses user_id instead of IP)
@router.post("/orders")
@rate_limit(limit=10, window=60, use_user_id=True)
async def create_order():
    pass
```

### Available Decorators

- `rate_limit(limit, window, use_user_id)` - Custom rate limit
- `rate_limit_auth(limit)` - For authentication endpoints
- `rate_limit_public(limit)` - For public endpoints
- `rate_limit_user(limit)` - For authenticated user endpoints
- `rate_limit_search(limit)` - For search endpoints

## Monitoring

### Check Rate Limit Status

```bash
curl http://localhost:8000/api/v1/rate-limit/status
```

Response:
```json
{
  "status": "success",
  "data": {
    "enabled": true,
    "storage_backend": "redis",
    "limits": {
      "global_per_hour": 1000,
      "auth_login_per_minute": 10,
      "public_per_minute": 100,
      ...
    },
    "whitelist_count": 2
  }
}
```

### Logs

Rate limit violations are logged:

```
WARNING - Rate limit exceeded for 192.168.1.100 on /api/v1/auth/login: 11/10 in 60s window
```

## Whitelisting IPs

To whitelist IPs (e.g., for monitoring tools, health checks):

```env
RATE_LIMIT_WHITELIST=127.0.0.1,::1,10.0.0.5,192.168.1.100
```

Whitelisted IPs bypass all rate limits.

## Storage Backends

### Redis (Production)

Recommended for production with multiple servers:

```env
RATE_LIMIT_STORAGE=redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-password
```

**Advantages:**
- Distributed rate limiting across multiple servers
- Persistent storage
- High performance

### In-Memory (Development)

Automatically used in development:

```env
RATE_LIMIT_STORAGE=memory
```

**Advantages:**
- No external dependencies
- Simple setup for local development

**Limitations:**
- Not suitable for multi-server deployments
- Resets on application restart

## Testing Rate Limits

### Manual Testing

```bash
# Test login rate limit (should fail after 10 requests)
for i in {1..15}; do
  curl -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"identifier":"test@example.com","password":"wrong"}'
  echo ""
done
```

### Check Headers

```bash
curl -i http://localhost:8000/api/v1/restaurants/nearby?latitude=19.0760&longitude=72.8777
```

Look for `X-RateLimit-*` headers in the response.

## Troubleshooting

### Rate Limits Not Working

1. Check if rate limiting is enabled:
   ```bash
   curl http://localhost:8000/api/v1/rate-limit/status
   ```

2. Verify Redis connection (if using Redis):
   ```bash
   curl http://localhost:8000/health
   ```

3. Check logs for errors:
   ```bash
   tail -f logs/app.log | grep -i "rate"
   ```

### False Positives

If legitimate users are being rate limited:

1. **Increase limits** via environment variables
2. **Whitelist IPs** for trusted sources
3. **Check for proxy issues** - ensure `X-Forwarded-For` header is properly configured

### Redis Connection Issues

If Redis fails, the system automatically falls back to in-memory storage:

```
WARNING - Failed to connect to Redis for rate limiting: Connection refused
WARNING - Falling back to in-memory storage
```

## Security Best Practices

1. **Use Redis in production** for distributed rate limiting
2. **Monitor rate limit violations** to detect potential attacks
3. **Adjust limits based on traffic patterns** - review and tune regularly
4. **Whitelist carefully** - only trusted IPs should bypass limits
5. **Enable HTTPS** - rate limiting works best with secure connections
6. **Log violations** - track patterns to identify malicious actors

## Performance Impact

Rate limiting adds minimal overhead:

- **Redis backend**: ~1-2ms per request
- **Memory backend**: <1ms per request
- **No impact** on whitelisted IPs or when disabled

## Future Enhancements

Potential improvements for future versions:

- [ ] Per-user customizable rate limits
- [ ] Dynamic rate limiting based on server load
- [ ] Rate limit analytics dashboard
- [ ] Automatic IP blocking after repeated violations
- [ ] Support for distributed rate limiting with Redis Cluster

## Support

For issues or questions about rate limiting:

1. Check logs: `logs/app.log`
2. Verify configuration: `/api/v1/rate-limit/status`
3. Review this documentation
4. Contact the development team

---

**Last Updated**: January 8, 2026  
**Version**: 1.0.0
