# Upstash Redis - Quick Reference Card

## 🚀 Quick Setup (5 Minutes)

### 1. Create Upstash Account
- Go to: https://upstash.com
- Sign up (free)
- Create Redis database (Regional, free tier)

### 2. Get Your Credentials
After creating database, copy:
```
Endpoint: redis-xxxxx-region.upstash.io
Port: 6379
Password: AXXXXXXXXXXXXXXXXXXx
```

### 3. Update .env File

**Local (.env)**:
```bash
REDIS_HOST=redis-xxxxx-region.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=AXXXXXXXXXXXXXXXXXXx
REDIS_USE_TLS=true
```

**EC2 (.env)**:
```bash
# SSH into EC2
ssh -i oneqlick-key-mumbai.pem ec2-user@your-ec2-ip

# Edit .env
nano /path/to/oneqlick-backend/.env

# Update Redis variables (same as above)
```

### 4. Deploy

```bash
# On EC2
cd /path/to/oneqlick-backend

# Stop containers
docker-compose -f docker-compose.prod.yml down

# Remove old Redis
docker volume rm oneqlick-backend_redis_data

# Restart (without Redis container)
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker logs oneqlick-backend | grep -i redis
```

### 5. Verify

```bash
# Should see in logs:
# ✅ "Successfully connected to Redis (TLS: True)"

# Test API
curl https://your-api.com/health
```

## 📊 Benefits

| Metric | Before (Docker Redis) | After (Upstash) |
|--------|----------------------|-----------------|
| **RAM Usage** | ~100MB | 0MB (external) |
| **Available RAM** | ~900MB | ~1000MB |
| **Performance** | Limited by EC2 | Optimized cloud |
| **Cost** | $0 | $0 (free tier) |

## 🔧 Troubleshooting

**Issue**: Connection failed
```bash
# Check TLS is enabled
grep REDIS_USE_TLS .env
# Should show: REDIS_USE_TLS=true
```

**Issue**: Wrong credentials
```bash
# Verify in Upstash dashboard
# Copy-paste carefully (no extra spaces)
```

**Rollback**: 
```bash
# Change .env back to:
REDIS_HOST=redis
REDIS_USE_TLS=false

# Restart with Redis container
docker-compose -f docker-compose.yml up -d
```

## 📈 Free Tier Limits

- **Commands**: 10,000/day ✅
- **Storage**: 256 MB ✅
- **Bandwidth**: 200 MB/day ✅

**Your Usage**: ~1,000-3,000 commands/day (well within limits)

## 🎯 Next Steps

After migration:
1. ✅ Monitor Upstash dashboard for 24h
2. ✅ Check EC2 memory usage (should drop)
3. ✅ Implement caching (see performance_analysis.md)
4. ✅ Consider upgrading EC2 to t3.small

---

**Questions?** Check UPSTASH_MIGRATION_GUIDE.md for detailed instructions.
