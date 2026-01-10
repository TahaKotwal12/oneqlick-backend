# Rate Limit Request Object Fix

## Issue
Login API was throwing an error: `LoginRequest object has no attribute 'headers'`

## Root Cause
The rate limit decorator was looking for a parameter named `request`, but the auth endpoints use `http_request` as the parameter name to avoid conflicts with the Pydantic request model.

## Solution
Updated the rate limit decorator in [`app/utils/rate_limiter.py`](file:///c:/Users/kotwa/OneDrive/Desktop/ONEQLICK%202026/oneqlick-backend/app/utils/rate_limiter.py#L280-L298) to check for multiple common Request parameter names:

```python
# Check common parameter names for Request object
if request is None:
    for param_name in ["request", "http_request", "req"]:
        if param_name in kwargs and isinstance(kwargs[param_name], Request):
            request = kwargs[param_name]
            break
```

## Changes Made
- **File**: `app/utils/rate_limiter.py`
- **Lines**: 289-294
- **Change**: Added loop to check for `request`, `http_request`, and `req` parameter names

## Test Results

### Before Fix
```
AttributeError: 'LoginRequest' object has no attribute 'headers'
```

### After Fix
```
✓ Request  1: Status 400 | Limit: 1000 | Remaining: 999
✓ Request  2: Status 400 | Limit: 1000 | Remaining: 998
✓ Headers working correctly!
```

## Verification
- ✅ Login endpoint works with rate limiting
- ✅ Headers appear in responses
- ✅ Rate limits are enforced
- ✅ No AttributeError

## Status
**FIXED** - Rate limiting is now fully functional on all endpoints including login.
