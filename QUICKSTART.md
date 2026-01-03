# OneQlick Backend - Quick Start Guide

## ✅ Docker Configuration Complete!

Your production-ready Docker setup is now complete with all necessary files.

## 🗄️ Database Configuration

Your Neon PostgreSQL database URL has been configured in:
- ✅ `docker-compose.yml` - for local Docker testing

**Database URL:**
```
postgresql://neondb_owner:npg_WU6NjGwae1bh@ep-cold-thunder-ad7m6qy2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## 🚀 Quick Start Commands

### 1. Test with Docker Compose (Recommended)

```bash
cd "c:\Users\kotwa\OneDrive\Desktop\ONEQLICK 2026\oneqlick-backend"

# Start the backend (connects to your Neon database)
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop
docker-compose down
```

### 2. Build Docker Image Only

```bash
# Build the production image
docker build -t oneqlick-backend .

# Run with your database
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://neondb_owner:npg_WU6NjGwae1bh@ep-cold-thunder-ad7m6qy2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require" \
  -e JWT_SECRET_KEY="your-secret-key" \
  oneqlick-backend
```

## 📦 What's Included

### Core Files
- ✅ `Dockerfile` - Production-optimized multi-stage build
- ✅ `.dockerignore` - Excludes unnecessary files
- ✅ `docker-compose.yml` - Local development with your Neon DB
- ✅ `requirements.txt` - Updated with gunicorn
- ✅ `gunicorn.conf.py` - Production server configuration

### Deployment Configs
- ✅ `railway.json` - Railway deployment config
- ✅ `aws/task-definition.json` - AWS ECS config
- ✅ `aws/ecs-params.yml` - ECS parameters
- ✅ `aws/buildspec.yml` - AWS CodeBuild config

### Documentation
- ✅ `DEPLOYMENT.md` - Complete deployment guide
- ✅ `DOCKER.md` - Docker commands reference

### Utilities
- ✅ `scripts/generate-secrets.py` - Generate secure keys
- ✅ `scripts/health-check.sh` - Health check script
- ✅ `.env.example` - Environment variable template

## 🎯 Next Steps

### Option 1: Deploy to Railway (Easiest)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Docker configuration"
   git push
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub
   - Add environment variables:
     - `DATABASE_URL` = your Neon URL (already configured)
     - `SECRET_KEY` = generate using `python scripts/generate-secrets.py`
     - `JWT_SECRET_KEY` = generate using `python scripts/generate-secrets.py`
   - Railway will auto-deploy!

### Option 2: Deploy to AWS ECS

Follow the detailed steps in `DEPLOYMENT.md`

### Option 3: Test Locally First

```bash
# Start with docker-compose
docker-compose up

# Test the API
curl http://localhost:8000/health

# View API docs
# Open browser: http://localhost:8000/docs
```

## 🔐 Important Security Notes

1. **Generate New Secret Keys** before deploying to production:
   ```bash
   python scripts/generate-secrets.py
   ```

2. **Never commit `.env` file** to Git (already in .gitignore)

3. **Use environment variables** in Railway/AWS, not hardcoded values

## 📱 Update Frontend Apps

After deployment, update the API URL in your frontend apps:

**File:** `oneqlick-partner-app/.env` and `oneQlick-User-App/.env`
```env
EXPO_PUBLIC_API_BASE_URL=https://your-railway-url.railway.app/api/v1
```

## 🆘 Troubleshooting

### Docker build fails
```bash
# Check Docker is running
docker --version

# Clean build
docker build --no-cache -t oneqlick-backend .
```

### Can't connect to database
- Verify the DATABASE_URL is correct
- Check if Neon database is accessible
- Test connection: `psql "postgresql://neondb_owner:..."`

### Port already in use
```bash
# Use different port
docker run -p 8080:8000 oneqlick-backend
```

## 📚 Documentation

- **Deployment Guide:** See `DEPLOYMENT.md`
- **Docker Reference:** See `DOCKER.md`
- **Environment Variables:** See `.env.example`

---

**🎉 Your backend is ready for deployment!**

Choose Railway for quick deployment or AWS for production-grade infrastructure.
