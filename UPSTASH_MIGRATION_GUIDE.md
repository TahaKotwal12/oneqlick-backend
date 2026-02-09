# Upstash Redis Migration Guide

## Overview
This guide will help you migrate from Docker Redis to Upstash's free Redis service, freeing up ~100MB RAM on your EC2 t3.micro instance.

---

## Step 1: Create Upstash Account (5 minutes)

1. Go to https://upstash.com
2. Click **"Sign Up"** or **"Get Started Free"**
3. Sign up with:
   - GitHub (recommended)
   - Google
   - Email

---

## Step 2: Create Redis Database (3 minutes)

1. After login, click **"Create Database"**
2. Configure:
   - **Name**: `oneqlick-redis`
   - **Type**: Select **"Regional"** (free tier)
   - **Region**: Choose closest to your EC2 (e.g., `us-east-1` for Mumbai choose `ap-south-1` if available)
   - **TLS**: ✅ Enabled (default)
   - **Eviction**: Select **"allkeys-lru"** (recommended)

3. Click **"Create"**

---

## Step 3: Get Connection Details

After creation, you'll see:

```
Endpoint: redis-12345-us-east-1.upstash.io
Port: 6379 (or 6380 for TLS)
Password: AXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
```

**Copy these values** - you'll need them in the next step.

---

## Step 4: Update Environment Variables

### On Your Local Machine

Edit `c:\Users\kotwa\OneDrive\Desktop\ONEQLICK 2026\oneqlick-backend\.env`:

```bash
# Redis Configuration - Upstash
REDIS_HOST=redis-12345-us-east-1.upstash.io  # Replace with your endpoint
REDIS_PORT=6379
REDIS_PASSWORD=AXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx  # Replace with your password
REDIS_USE_TLS=true  # NEW - Enable TLS for Upstash
REDIS_TTL=300
REDIS_NAMESPACE=oneqlick
REDIS_TIMEOUT_MS=10000
```

### On Your EC2 Instance

SSH into your EC2 instance:

```bash
ssh -i oneqlick-key-mumbai.pem ec2-user@your-ec2-ip
```

Edit the `.env` file:

```bash
cd /path/to/oneqlick-backend
nano .env

# Update the same Redis variables as above
# Save: Ctrl+O, Enter, Ctrl+X
```

---

## Step 5: Update Redis Repository Code

The code changes are already prepared. Review the updated file:
- `app/infra/redis/repositories/redis_repositories.py`

Key changes:
- Added TLS/SSL support for Upstash
- Added connection retry logic
- Improved error handling

---

## Step 6: Update Docker Compose (Remove Redis Container)

### For Production Deployment

Edit `docker-compose.prod.yml` to remove Redis service (already updated).

The Redis container will no longer run, freeing up ~100MB RAM.

---

## Step 7: Update .env.example (Documentation)

Updated `.env.example` to include Upstash configuration for future reference.

---

## Step 8: Deploy Changes

### Option A: If Using Docker Compose on EC2

```bash
# SSH into EC2
ssh -i oneqlick-key-mumbai.pem ec2-user@your-ec2-ip

# Navigate to project
cd /path/to/oneqlick-backend

# Pull latest changes (if using Git)
git pull origin main

# Stop and remove old containers
docker-compose -f docker-compose.prod.yml down

# Remove Redis container and volumes
docker-compose -f docker-compose.prod.yml rm -f redis
docker volume rm oneqlick-backend_redis_data

# Rebuild and restart (without Redis)
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Option B: If Using GitHub Actions CI/CD

```bash
# Commit and push changes
git add .
git commit -m "Migrate to Upstash Redis"
git push origin main

# GitHub Actions will automatically deploy
# Monitor deployment in GitHub Actions tab
```

---

## Step 9: Verify Connection

### Test Redis Connection

```bash
# SSH into EC2
ssh -i oneqlick-key-mumbai.pem ec2-user@your-ec2-ip

# Check backend logs
docker logs oneqlick-backend

# Look for:
# ✅ "Successfully connected to Redis"
# ❌ "Failed to initialize Redis client"
```

### Test API Endpoint

```bash
# Test health check
curl https://your-api-domain.com/health

# Should return:
{
  "status": "healthy",
  "redis": "connected",
  ...
}
```

### Test Rate Limiting (Uses Redis)

```bash
# Make multiple requests to trigger rate limit
for i in {1..15}; do
  curl -X POST https://your-api-domain.com/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"test"}'
done

# Should eventually return 429 Too Many Requests
```

---

## Step 10: Monitor Upstash Dashboard

1. Go to https://console.upstash.com
2. Click on your `oneqlick-redis` database
3. Monitor:
   - **Commands/day**: Should stay under 10,000 for free tier
   - **Storage**: Should stay under 256 MB
   - **Connections**: Should show active connections

---

## Rollback Plan (If Something Goes Wrong)

If Upstash connection fails, you can quickly rollback:

### 1. Revert .env Changes

```bash
# Change back to Docker Redis
REDIS_HOST=redis  # or localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_USE_TLS=false
```

### 2. Restart Docker Redis

```bash
# Uncomment Redis service in docker-compose.prod.yml
# Then restart
docker-compose -f docker-compose.prod.yml up -d redis
docker-compose -f docker-compose.prod.yml restart backend
```

---

## Expected Benefits

After migration:

✅ **~100MB RAM freed** on EC2 instance
✅ **Better Redis performance** (managed service)
✅ **No Redis maintenance** needed
✅ **Automatic backups** (Upstash handles this)
✅ **Better monitoring** (Upstash dashboard)

---

## Troubleshooting

### Issue: "Failed to connect to Redis"

**Solution 1**: Check TLS setting
```python
# Make sure REDIS_USE_TLS=true in .env
```

**Solution 2**: Check firewall
```bash
# Test connection from EC2
telnet redis-12345-us-east-1.upstash.io 6379
```

**Solution 3**: Verify credentials
```bash
# Double-check REDIS_HOST, REDIS_PORT, REDIS_PASSWORD in .env
```

### Issue: "SSL: CERTIFICATE_VERIFY_FAILED"

**Solution**: Update redis-py library
```bash
pip install --upgrade redis
```

### Issue: Rate limiting not working

**Solution**: Check Redis connection in logs
```bash
docker logs oneqlick-backend | grep -i redis
```

---

## Cost Monitoring

### Free Tier Limits
- **Commands**: 10,000/day
- **Storage**: 256 MB
- **Bandwidth**: 200 MB/day

### Typical Usage (OneQlick Backend)
- **Rate limiting**: ~100-500 commands/day
- **Caching**: ~500-2000 commands/day
- **Total**: ~1000-3000 commands/day ✅ Well within free tier

### If You Exceed Free Tier
- **Pay-as-you-go**: $0.20 per 100K commands
- **Pro Plan**: $10/month for 1M commands/day

---

## Next Steps After Migration

1. ✅ Monitor Upstash dashboard for 24 hours
2. ✅ Check EC2 memory usage (should drop by ~100MB)
3. ✅ Implement caching (from performance analysis)
4. ✅ Consider upgrading EC2 to t3.small

---

## Support

- **Upstash Docs**: https://docs.upstash.com/redis
- **Upstash Discord**: https://discord.gg/upstash
- **Issue**: Create issue in your GitHub repo

---

**Estimated Migration Time**: 20-30 minutes
**Downtime**: ~2-5 minutes (during container restart)
**Risk Level**: Low (easy rollback)

Good luck! 🚀
