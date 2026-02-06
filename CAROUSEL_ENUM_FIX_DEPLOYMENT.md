# Carousel Enum Fix - Deployment Guide

## Problem
The carousel API was returning a 500 error because SQLAlchemy's Enum handling was using Python enum attribute names (UPPERCASE) instead of the database enum values (lowercase).

## Root Cause
In `app/infra/db/postgres/models/coupon.py`, line 17:
```python
# OLD (BROKEN):
coupon_type = Column(Enum(CouponType), nullable=False)

# NEW (FIXED):
coupon_type = Column(Enum(CouponType, native_enum=True, name='coupontype', create_constraint=True, validate_strings=True), nullable=False)
```

## What Changed
- Added `native_enum=True` to use the existing database enum type
- Added `name='coupontype'` to explicitly reference the database enum
- Added `validate_strings=True` to ensure proper validation

## Deployment Steps

### 1. Commit and Push Changes
```bash
cd oneqlick-backend
git add app/infra/db/postgres/models/coupon.py
git commit -m "fix: SQLAlchemy enum handling for coupon_type to use database native enum"
git push origin main
```

### 2. Deploy to AWS

#### Option A: If using Docker on AWS
```bash
# SSH into AWS
ssh your-aws-server

# Navigate to backend directory
cd /path/to/oneqlick-backend

# Pull latest changes
git pull origin main

# Rebuild and restart the container
docker-compose down app
docker-compose build app
docker-compose up -d app

# Check logs
docker-compose logs -f app
```

#### Option B: If using direct deployment
```bash
# SSH into AWS
ssh your-aws-server

# Navigate to backend directory
cd /path/to/oneqlick-backend

# Pull latest changes
git pull origin main

# Restart the service
sudo systemctl restart oneqlick-backend
# OR
pm2 restart oneqlick-backend

# Check logs
sudo journalctl -u oneqlick-backend -f
# OR
pm2 logs oneqlick-backend
```

### 3. Verify the Fix
After deployment, test the carousel API:
```bash
curl https://api.oneqlick.in/api/v1/coupons/carousel
```

Expected response:
```json
{
  "code": 200,
  "data": {
    "coupons": [...],
    "total_count": 5
  },
  "message": "Carousel coupons retrieved successfully"
}
```

### 4. Test on Mobile App
- Refresh the mobile app
- The carousel should now load successfully
- You should see 5 carousel items with proper gradients and data

## Files Modified
- `app/infra/db/postgres/models/coupon.py` - Fixed enum handling

## Database State
- ✅ Enum definition: `percentage`, `fixed_amount`, `free_delivery` (lowercase)
- ✅ Data: 5 carousel coupons with lowercase enum values
- ✅ No migration needed - only code change

## Rollback (if needed)
```bash
git revert HEAD
git push origin main
# Then redeploy
```
