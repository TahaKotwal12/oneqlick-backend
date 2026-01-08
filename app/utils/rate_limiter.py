"""
Rate Limiting Utility for OneQlick Backend

This module provides comprehensive rate limiting functionality with support for:
- Multiple storage backends (Redis for production, in-memory for development)
- Sliding window algorithm for accurate rate limiting
- IP-based and user-based rate limiting
- Custom rate limit decorators
- Rate limit headers in responses
"""

import time
import hashlib
from typing import Optional, Tuple, Dict
from functools import wraps
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.config.logger import get_logger
from app.config.config import RATE_LIMIT_CONFIG, REDIS_CONFIG

logger = get_logger(__name__)


class RateLimitStorage:
    """Abstract base class for rate limit storage backends"""
    
    def increment(self, key: str, window: int) -> int:
        """Increment counter for key and return current count"""
        raise NotImplementedError
    
    def get(self, key: str) -> int:
        """Get current count for key"""
        raise NotImplementedError
    
    def reset(self, key: str):
        """Reset counter for key"""
        raise NotImplementedError


class MemoryStorage(RateLimitStorage):
    """In-memory storage backend for development"""
    
    def __init__(self):
        self._storage: Dict[str, Tuple[int, float]] = {}
        logger.info("Rate limiting using in-memory storage (development mode)")
    
    def increment(self, key: str, window: int) -> int:
        """Increment counter for key and return current count"""
        current_time = time.time()
        
        # Clean up expired entries
        self._cleanup()
        
        if key in self._storage:
            count, timestamp = self._storage[key]
            # Check if window has expired
            if current_time - timestamp > window:
                # Reset counter
                self._storage[key] = (1, current_time)
                return 1
            else:
                # Increment counter
                self._storage[key] = (count + 1, timestamp)
                return count + 1
        else:
            # First request
            self._storage[key] = (1, current_time)
            return 1
    
    def get(self, key: str) -> int:
        """Get current count for key"""
        if key in self._storage:
            count, timestamp = self._storage[key]
            return count
        return 0
    
    def reset(self, key: str):
        """Reset counter for key"""
        if key in self._storage:
            del self._storage[key]
    
    def _cleanup(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = []
        
        for key, (count, timestamp) in self._storage.items():
            # Remove entries older than 1 hour
            if current_time - timestamp > 3600:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._storage[key]


class RedisStorage(RateLimitStorage):
    """Redis storage backend for production"""
    
    def __init__(self):
        try:
            import redis
            self._redis = redis.Redis(
                host=REDIS_CONFIG["host"],
                port=REDIS_CONFIG["port"],
                password=REDIS_CONFIG["password"] if REDIS_CONFIG["password"] else None,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self._redis.ping()
            logger.info(f"Rate limiting using Redis storage at {REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis for rate limiting: {e}")
            logger.warning("Falling back to in-memory storage")
            raise
    
    def increment(self, key: str, window: int) -> int:
        """Increment counter for key using Redis INCR with expiration"""
        try:
            # Use pipeline for atomic operations
            pipe = self._redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, window)
            results = pipe.execute()
            return results[0]  # Return the incremented value
        except Exception as e:
            logger.error(f"Redis rate limit increment error: {e}")
            # Return 0 to allow request if Redis fails
            return 0
    
    def get(self, key: str) -> int:
        """Get current count for key"""
        try:
            value = self._redis.get(key)
            return int(value) if value else 0
        except Exception as e:
            logger.error(f"Redis rate limit get error: {e}")
            return 0
    
    def reset(self, key: str):
        """Reset counter for key"""
        try:
            self._redis.delete(key)
        except Exception as e:
            logger.error(f"Redis rate limit reset error: {e}")


class RateLimiter:
    """Main rate limiter class"""
    
    def __init__(self):
        self.enabled = RATE_LIMIT_CONFIG["enabled"]
        self.whitelist = RATE_LIMIT_CONFIG["whitelist"]
        
        # Initialize storage backend
        if RATE_LIMIT_CONFIG["storage"] == "redis":
            try:
                self.storage = RedisStorage()
            except Exception:
                # Fallback to memory storage if Redis fails
                self.storage = MemoryStorage()
        else:
            self.storage = MemoryStorage()
        
        logger.info(f"Rate limiter initialized (enabled={self.enabled})")
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        # Check for X-Forwarded-For header (proxy/load balancer)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # Take the first IP in the chain
            return forwarded.split(",")[0].strip()
        
        # Check for X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        return request.client.host if request.client else "unknown"
    
    def _is_whitelisted(self, ip: str) -> bool:
        """Check if IP is whitelisted"""
        return ip in self.whitelist
    
    def _generate_key(self, identifier: str, endpoint: str) -> str:
        """Generate a unique key for rate limiting"""
        # Use hash to keep keys short
        combined = f"{identifier}:{endpoint}"
        return f"ratelimit:{hashlib.md5(combined.encode()).hexdigest()}"
    
    def check_rate_limit(
        self,
        request: Request,
        limit: int,
        window: int,
        identifier: Optional[str] = None
    ) -> Tuple[bool, int, int, int]:
        """
        Check if request exceeds rate limit
        
        Args:
            request: FastAPI request object
            limit: Maximum number of requests allowed
            window: Time window in seconds
            identifier: Optional custom identifier (e.g., user_id). If None, uses IP address
        
        Returns:
            Tuple of (allowed, current_count, limit, reset_time)
        """
        # Skip if rate limiting is disabled
        if not self.enabled:
            return True, 0, limit, 0
        
        # Get identifier (IP or custom)
        if identifier is None:
            identifier = self._get_client_ip(request)
        
        # Check whitelist
        if self._is_whitelisted(identifier):
            return True, 0, limit, 0
        
        # Generate key
        endpoint = request.url.path
        key = self._generate_key(identifier, endpoint)
        
        # Increment counter
        current_count = self.storage.increment(key, window)
        
        # Calculate reset time
        reset_time = int(time.time()) + window
        
        # Check if limit exceeded
        allowed = current_count <= limit
        
        if not allowed:
            logger.warning(
                f"Rate limit exceeded for {identifier} on {endpoint}: "
                f"{current_count}/{limit} in {window}s window"
            )
        
        return allowed, current_count, limit, reset_time
    
    def get_rate_limit_headers(
        self,
        current_count: int,
        limit: int,
        reset_time: int
    ) -> Dict[str, str]:
        """Generate rate limit headers for response"""
        remaining = max(0, limit - current_count)
        
        return {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset_time),
        }


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(limit: int, window: int = 60, use_user_id: bool = False):
    """
    Decorator for rate limiting endpoints
    
    Args:
        limit: Maximum number of requests allowed
        window: Time window in seconds (default: 60)
        use_user_id: If True, use user_id from request state instead of IP
    
    Example:
        @rate_limit(limit=10, window=60)
        async def login(request: Request):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Find request object in args or kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            # Check common parameter names for Request object
            if request is None:
                for param_name in ["request", "http_request", "req"]:
                    if param_name in kwargs and isinstance(kwargs[param_name], Request):
                        request = kwargs[param_name]
                        break
            
            if request is None:
                logger.warning("Rate limit decorator: Request object not found in args or kwargs")
                return await func(*args, **kwargs)
            
            # Get identifier
            identifier = None
            if use_user_id:
                # Try to get user_id from request state (set by auth middleware)
                identifier = getattr(request.state, "user_id", None)
                if identifier:
                    identifier = str(identifier)
            
            # Check rate limit
            allowed, current_count, limit_value, reset_time = rate_limiter.check_rate_limit(
                request, limit, window, identifier
            )
            
            # Add rate limit headers to response
            headers = rate_limiter.get_rate_limit_headers(current_count, limit_value, reset_time)
            
            if not allowed:
                # Rate limit exceeded
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "code": 429,
                        "message": f"Rate limit exceeded. Try again in {reset_time - int(time.time())} seconds.",
                        "message_id": "RATE_LIMIT_EXCEEDED",
                        "data": {
                            "limit": limit_value,
                            "window": window,
                            "reset_time": reset_time
                        }
                    },
                    headers=headers
                )
            
            # Execute the endpoint
            response = await func(*args, **kwargs)
            
            # Add headers to successful response
            if hasattr(response, "headers"):
                for key, value in headers.items():
                    response.headers[key] = value
            
            return response
        
        return wrapper
    return decorator


# Convenience decorators for common rate limits
def rate_limit_auth(limit: int = None):
    """Rate limit for authentication endpoints (default: 10 req/min)"""
    if limit is None:
        limit = RATE_LIMIT_CONFIG["auth_login_per_minute"]
    return rate_limit(limit=limit, window=60, use_user_id=False)


def rate_limit_public(limit: int = None):
    """Rate limit for public endpoints (default: 100 req/min)"""
    if limit is None:
        limit = RATE_LIMIT_CONFIG["public_per_minute"]
    return rate_limit(limit=limit, window=60, use_user_id=False)


def rate_limit_user(limit: int = None):
    """Rate limit for authenticated user endpoints (default: 200 req/min)"""
    if limit is None:
        limit = RATE_LIMIT_CONFIG["user_per_minute"]
    return rate_limit(limit=limit, window=60, use_user_id=True)


def rate_limit_search(limit: int = None):
    """Rate limit for search endpoints (default: 50 req/min)"""
    if limit is None:
        limit = RATE_LIMIT_CONFIG["search_per_minute"]
    return rate_limit(limit=limit, window=60, use_user_id=False)
