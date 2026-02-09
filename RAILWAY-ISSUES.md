# Railway Deployment - Known Issues & Solutions

## Issue 1: Redis Connection Warnings ⚠️

**Symptom:**
```
WARNING - Redis connection failed: Error 111 connecting to localhost:6379
```

**Cause:** Railway doesn't have Redis by default, and the app tries to connect to localhost.

**Solution:** Redis is **optional** for the app. The warnings are harmless.

**To Fix (Optional):**
1. Add Redis to Railway:
   - Click "New" → "Database" → "Redis"
   - Railway will provide `REDIS_URL`
2. Add environment variable:
   ```
   REDIS_HOST=<from Railway Redis service>
   REDIS_PORT=6379
   ```

**Or ignore it** - the app works fine without Redis.

---

## Issue 2: Worker Timeout During Email Sending 🔴

**Symptom:**
```
[CRITICAL] WORKER TIMEOUT (pid:X)
```

**Cause:** Gmail SMTP can be slow (2+ minutes), causing gunicorn workers to timeout.

**Solution Applied:**
- ✅ Increased timeout from 120s to 300s in `gunicorn.conf.py` and `Dockerfile`

**If still timing out:**
1. Use a faster email service (SendGrid, Mailgun)
2. Or implement async email sending with Celery/background tasks

---

## Issue 3: Gmail SMTP "Less Secure Apps"

**Symptom:** Email not sending even after timeout fix.

**Solution:**
1. Enable 2-Factor Authentication on Gmail
2. Generate an **App Password**:
   - Go to Google Account → Security → 2-Step Verification → App Passwords
   - Create new app password
   - Use that password in `SMTP_PASSWORD` instead of your regular password

---

## Current Status

✅ Database: Connected (Neon PostgreSQL)  
⚠️ Redis: Not connected (optional, safe to ignore)  
🔄 Email: Timeout increased to 300s  

**Next Steps:**
1. Rebuild and push Docker image
2. Redeploy on Railway
3. Test email sending

---

**Quick Commands:**
```bash
# Rebuild and push
docker build -t oneqlick-backend .
docker tag oneqlick-backend tahakotwal/oneqlick-backend-app:latest
docker push tahakotwal/oneqlick-backend-app:latest

# Then redeploy on Railway dashboard
```
