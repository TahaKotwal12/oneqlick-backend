# Docker Push & Deploy - Quick Reference

## Push Updated Image to Docker Hub

```bash
# 1. Build new image
docker build -t oneqlick-backend .

# 2. Tag for Docker Hub
docker tag oneqlick-backend tahakotwal/oneqlick-backend-app:latest

# 3. Push to Docker Hub
docker push tahakotwal/oneqlick-backend-app:latest
```

## Deploy on Railway

### Method 1: Railway Dashboard
1. Go to your Railway project
2. Click "Redeploy" (Railway auto-pulls latest image)

### Method 2: Railway CLI
```bash
railway up
```

---

**That's it!** Railway will automatically pull the new image and redeploy.
