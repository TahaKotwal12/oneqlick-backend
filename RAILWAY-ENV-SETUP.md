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

## Important: Environment Variables on Railway

Make sure these are set in Railway Variables:

**Required:**
- `DATABASE_URL` - Your Neon PostgreSQL URL
- `SECRET_KEY` - Your app secret key
- `JWT_SECRET_KEY` - Your JWT secret key

**Email Service (SendGrid - Recommended):**
- `SENDGRID_API_KEY=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`
- `SENDGRID_FROM_EMAIL=noreply@oneqlick.com`

**Email Service (SMTP - Not Recommended for Railway):**
- `SMTP_HOST=smtp.gmail.com`
- `SMTP_PORT=587`
- `SMTP_USERNAME=oneqlick01@gmail.com`
- `SMTP_PASSWORD=lnbd npah ehre fbeq`
- `SMTP_USE_TLS=true`

**SMS Service (if using):**
- `TWILIO_ACCOUNT_SID=AC435aaf3b919674dc8fd91bce2edfc5e6`
- `TWILIO_AUTH_TOKEN=06bd88b2225235b37d9c312a25333c21`
- `TWILIO_PHONE_NUMBER=+14342265098`

**Other:**
- `APP_ENV=production`
- `DEBUG=false`
- `PORT=8000`

---

**That's it!** Railway will automatically pull the new image and redeploy with your environment variables.
