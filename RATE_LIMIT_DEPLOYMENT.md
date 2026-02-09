# Rate Limit Fix - Parameter Order

## Problem
Login and other auth endpoints were throwing:
```
AttributeError: 'LoginRequest' object has no attribute 'headers'
```

## Root Cause
The rate limit decorator was finding the Pydantic `LoginRequest` model before the FastAPI `Request` object because they were in the wrong order in the function parameters.

## Solution
Reordered function parameters to put `http_request: Request` (FastAPI Request) **before** the Pydantic request models.

## Files Changed

### 1. `app/utils/rate_limiter.py`
- Added checks for `hasattr(arg, 'headers')` and `hasattr(arg, 'client')` to ensure we find the FastAPI Request, not Pydantic models
- Check kwargs in order: `["http_request", "request", "req"]` (prioritizing `http_request`)

### 2. `app/api/routes/auth.py`
Fixed parameter order in 3 endpoints:

**Login endpoint (line 36-39):**
```python
# BEFORE:
async def login(
    request: LoginRequest,
    http_request: Request,
    ...
)

# AFTER:
async def login(
    http_request: Request,
    request: LoginRequest,
    ...
)
```

**Signup endpoint (line 119-122):**
```python
# BEFORE:
async def signup(
    request: SignupRequest,
    http_request: Request,
    ...
)

# AFTER:
async def signup(
    http_request: Request,
    request: SignupRequest,
    ...
)
```

**Forgot Password endpoint (line 613-615):**
```python
# BEFORE:
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
)

# AFTER:
async def forgot_password(
    http_request: Request,
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
)
```

## Deployment Steps

1. **Commit changes:**
   ```bash
   git add .
   git commit -m "fix: reorder auth endpoint parameters for rate limiting"
   git push origin main
   ```

2. **GitHub Actions will automatically deploy to AWS EC2**

3. **Verify deployment:**
   - Check GitHub Actions workflow status
   - Test login endpoint
   - Verify no more AttributeError

## Testing
After deployment, test with:
```bash
curl -X POST https://your-api.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"test@example.com","password":"test123"}'
```

Should return proper error (401/400) instead of 500 AttributeError.

## Status
✅ **READY TO DEPLOY** - All changes committed locally, ready to push to GitHub
