# OneQlick Backend - AWS EC2 Deployment Guide

Complete guide for deploying the OneQlick FastAPI backend to AWS EC2 Mumbai with automated CI/CD and scheduled start/stop.

---

## 📋 Deployment Overview

**Infrastructure:**
- **Compute**: AWS EC2 t3.micro (Mumbai - ap-south-1)
- **Database**: Neon DB PostgreSQL (Free Tier)
- **Cache**: Upstash Redis (Free Tier)
- **CI/CD**: GitHub Actions
- **Cost**: $0-5/month (Free Tier optimized)

**Live API**: http://3.109.40.217:8000/api/v1

---

## 🚀 Complete Deployment Steps

### Step 1: AWS EC2 Setup

#### 1.1 Create Security Group

```bash
# Set region
export AWS_REGION=ap-south-1

# Create security group
aws ec2 create-security-group \
    --group-name oneqlick-backend-sg \
    --description "Security group for OneQlick Backend" \
    --region $AWS_REGION

# Get security group ID
SG_ID=$(aws ec2 describe-security-groups \
    --group-names oneqlick-backend-sg \
    --query 'SecurityGroups[0].GroupId' \
    --output text \
    --region $AWS_REGION)

# Allow SSH (port 22)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0 \
    --region $AWS_REGION

# Allow HTTP (port 80)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0 \
    --region $AWS_REGION

# Allow HTTPS (port 443)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0 \
    --region $AWS_REGION

# Allow port 8000 (Application)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0 \
    --region $AWS_REGION
```

#### 1.2 Create SSH Key Pair

```bash
# Create key pair
aws ec2 create-key-pair \
    --key-name oneqlick-key-mumbai \
    --query 'KeyMaterial' \
    --output text \
    --region ap-south-1 > oneqlick-key-mumbai.pem

# Set permissions
chmod 400 oneqlick-key-mumbai.pem
```

#### 1.3 Launch EC2 Instance

```bash
# Get latest Ubuntu AMI
AMI_ID=$(aws ec2 describe-images \
    --owners 099720109477 \
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
    --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
    --output text \
    --region ap-south-1)

# Launch instance
aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type t3.micro \
    --key-name oneqlick-key-mumbai \
    --security-group-ids $SG_ID \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=oneqlick-backend-mumbai}]' \
    --region ap-south-1

# Get instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=oneqlick-backend-mumbai" \
    --query 'Reservations[0].Instances[0].InstanceId' \
    --output text \
    --region ap-south-1)

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region ap-south-1
```

#### 1.4 Allocate Elastic IP

```bash
# Allocate Elastic IP
ALLOCATION_ID=$(aws ec2 allocate-address \
    --domain vpc \
    --query 'AllocationId' \
    --output text \
    --region ap-south-1)

# Associate with instance
aws ec2 associate-address \
    --instance-id $INSTANCE_ID \
    --allocation-id $ALLOCATION_ID \
    --region ap-south-1

# Get Elastic IP
ELASTIC_IP=$(aws ec2 describe-addresses \
    --allocation-ids $ALLOCATION_ID \
    --query 'Addresses[0].PublicIp' \
    --output text \
    --region ap-south-1)

echo "Elastic IP: $ELASTIC_IP"
# Output: 3.109.40.217
```

---

### Step 2: EC2 Instance Configuration

#### 2.1 Connect to EC2

**Option 1: AWS Console (Easiest)**
1. Go to EC2 Console: https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#Instances:
2. Select instance → Click **Connect** → **EC2 Instance Connect** → **Connect**

**Option 2: SSH**
```bash
ssh -i oneqlick-key-mumbai.pem ubuntu@3.109.40.217
```

#### 2.2 Install Docker

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Enable Docker
sudo systemctl enable docker
sudo systemctl start docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

#### 2.3 Clone Repository

```bash
# Clone from GitHub
cd ~
git clone https://github.com/TahaKotwal12/oneqlick-backend.git
cd oneqlick-backend
```

#### 2.4 Create Production Environment File

```bash
# Create .env file
nano .env
```

Paste the following configuration:

```env
# Application
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Security
SECRET_KEY=u1SJF54oGY1HsLbdBd5Oa4-73GBLEojhW2MBxzhJwsA
JWT_SECRET_KEY=sAa8NxOeFKGZymT5-oMIBMcYvgbW2x5H9gfxStc7X8DC3nToujJs_uy7Xc9p2ZXlIuJb2be5FPfCRLmqYtWgWg
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
BCRYPT_ROUNDS=12
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_NUMBERS=true
PASSWORD_REQUIRE_SPECIAL_CHARS=true

# Neon Database
DATABASE_URL=postgresql://neondb_owner:npg_WU6NjGwae1bh@ep-cold-thunder-ad7m6qy2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
DB_POOL_MAX_SIZE=10
DB_POOL_MIN_IDLE=1
DB_POOL_IDLE_TIMEOUT=30000
DB_POOL_MAX_LIFETIME=1800000
DB_POOL_CONNECTION_TIMEOUT=30000
DB_POOL_NAME=OneQlickFoodDeliveryCP

# Upstash Redis
UPSTASH_REDIS_REST_URL=https://sought-grub-32496.upstash.io
UPSTASH_REDIS_REST_TOKEN=AX7wAAIncDI2MGI2MjkwMjc3MDg0ZDhiOTJkODE5OWVhN2ZhMmRmOXAyMzI0OTY
REDIS_HOST=sought-grub-32496.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=AX7wAAIncDI2MGI2MjkwMjc3MDg0ZDhiOTJkODE5OWVhN2ZhMmRmOXAyMzI0OTY
REDIS_TTL=300
REDIS_NAMESPACE=oneqlick
REDIS_TIMEOUT_MS=10000
REDIS_MAX_ACTIVE=20
REDIS_MAX_IDLE=5
REDIS_MIN_IDLE=1

# CORS
CORS_ORIGINS=*
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS,PATCH
CORS_HEADERS=*

# Email (Gmail SMTP)
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=oneqlick01@gmail.com
SMTP_PASSWORD=lnbd npah ehre fbeq
SMTP_USE_TLS=true

# SMS (Twilio)
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=AC435aaf3b919674dc8fd91bce2edfc5e6
TWILIO_AUTH_TOKEN=06bd88b2225235b37d9c312a25333c21
TWILIO_PHONE_NUMBER=+14342265098

# Google OAuth
GOOGLE_CLIENT_ID=1024710005377-603b3r4u26tgehu0nc1d9frjb1j0v1u9.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=
GOOGLE_PROJECT_ID=pragmatic-braid-445409-h4

# File Upload
UPLOAD_MAX_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,pdf,doc,docx
UPLOAD_PATH=uploads

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Logging
SENTRY_DSN=
LOG_FILE_PATH=logs/app.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5
```

Save: `Ctrl+X`, `Y`, `Enter`

#### 2.5 Build and Run Docker Container

```bash
# Build Docker image
docker build -t oneqlick-backend .

# Run container
docker run -d \
    --name oneqlick-backend \
    --restart unless-stopped \
    -p 8000:8000 \
    --env-file .env \
    oneqlick-backend

# Check status
docker ps

# View logs
docker logs -f oneqlick-backend
```

#### 2.6 Test Deployment

```bash
# Test from EC2
curl http://localhost:8000/health

# Test from local machine
curl http://3.109.40.217:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "OneQlick Backend",
  "database": "connected",
  "redis": "connected",
  "batch_cleanup": "running"
}
```

---

### Step 3: CI/CD with GitHub Actions

#### 3.1 Generate SSH Key for GitHub Actions

On EC2:
```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_actions_key -N ""

# Add public key to authorized_keys
cat ~/.ssh/github_actions_key.pub >> ~/.ssh/authorized_keys

# Display private key (copy this for GitHub)
cat ~/.ssh/github_actions_key
```

#### 3.2 Configure GitHub Secrets

Go to: https://github.com/TahaKotwal12/oneqlick-backend/settings/secrets/actions

Add these 3 secrets:

| Secret Name | Value |
|-------------|-------|
| `EC2_HOST` | `3.109.40.217` |
| `EC2_USERNAME` | `ubuntu` |
| `EC2_SSH_KEY` | [Full private key from step 3.1] |

#### 3.3 GitHub Actions Workflow

File: `.github/workflows/deploy.yml`

```yaml
name: Deploy to EC2 Mumbai

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/oneqlick-backend
            git pull origin main
            docker-compose down
            docker-compose build
            docker-compose up -d
            docker ps
            echo "Deployment completed successfully!"
```

#### 3.4 Production Docker Compose

File: `docker-compose.prod.yml`

```yaml
version: '3.8'

services:
  backend:
    build: .
    container_name: oneqlick-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Link it:
```bash
ln -sf docker-compose.prod.yml docker-compose.yml
```

---

### Step 4: Automated Start/Stop Schedule

#### 4.1 Create EventBridge Rules

**START Rule (9 AM IST):**

1. Go to EventBridge: https://ap-south-1.console.aws.amazon.com/events/home?region=ap-south-1#/rules
2. Click **Create rule**
3. Configure:
   - **Name**: `start-oneqlick-9am`
   - **Description**: `Start EC2 at 9 AM IST daily`
   - **Rule type**: Schedule
   - **Cron expression**: `30 3 * * ? *` (3:30 AM UTC = 9:00 AM IST)
   - **Target**: EC2 StartInstances API call
   - **Instance ID**: `i-046d8c6492a4cd3fc`

**STOP Rule (10 PM IST):**

1. Click **Create rule**
2. Configure:
   - **Name**: `stop-oneqlick-10pm`
   - **Description**: `Stop EC2 at 10 PM IST daily`
   - **Rule type**: Schedule
   - **Cron expression**: `30 16 * * ? *` (4:30 PM UTC = 10:00 PM IST)
   - **Target**: EC2 StopInstances API call
   - **Instance ID**: `i-046d8c6492a4cd3fc`

---

## 📱 Mobile App Configuration

Update API URL in both mobile apps:

**oneQlick-User-App/.env:**
```env
EXPO_PUBLIC_API_BASE_URL=http://3.109.40.217:8000/api/v1
```

**oneQlick-Partner-App/.env:**
```env
EXPO_PUBLIC_API_BASE_URL=http://3.109.40.217:8000/api/v1
```

Restart Expo:
```bash
npx expo start --clear
```

---

## 🔧 Maintenance Commands

### View Logs
```bash
docker logs -f oneqlick-backend
# or
docker-compose logs -f
```

### Restart Backend
```bash
docker-compose restart
```

### Update Code
```bash
cd ~/oneqlick-backend
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

### Check System Resources
```bash
docker stats oneqlick-backend
free -h
df -h
```

### Manual Start/Stop
```bash
# Stop instance
aws ec2 stop-instances --instance-ids i-046d8c6492a4cd3fc --region ap-south-1

# Start instance
aws ec2 start-instances --instance-ids i-046d8c6492a4cd3fc --region ap-south-1
```

---

## 🔗 Important URLs

- **API Base**: http://3.109.40.217:8000/api/v1
- **Health Check**: http://3.109.40.217:8000/health
- **API Docs**: http://3.109.40.217:8000/docs
- **ReDoc**: http://3.109.40.217:8000/redoc
- **GitHub Repo**: https://github.com/TahaKotwal12/oneqlick-backend
- **EC2 Console**: https://ap-south-1.console.aws.amazon.com/ec2/home?region=ap-south-1#Instances:

---

## 💰 Cost Optimization

**Current Setup:**
- EC2 t3.micro: **$0** (Free Tier - 750 hours/month for 12 months)
- Neon DB: **$0** (Free Tier - 0.5 GB storage)
- Upstash Redis: **$0** (Free Tier - 10k commands/day)
- Elastic IP: **$0** (Free when attached to running instance)
- Auto Schedule: **Saves 47%** (runs 13 hours/day instead of 24)

**Estimated Monthly Cost**: $0-5/month  
**$100 Credits Duration**: 6-12 months

---

## 🛡️ Security Best Practices

1. **Rotate Keys**: Change SSH keys and secrets regularly
2. **Update System**: Run `sudo apt update && sudo apt upgrade` monthly
3. **Monitor Logs**: Check logs for suspicious activity
4. **Backup Database**: Neon DB has automatic backups
5. **Use HTTPS**: Add SSL certificate for production (optional)

---

## 📊 Deployment Summary

| Component | Configuration |
|-----------|--------------|
| **Region** | Mumbai (ap-south-1) |
| **Instance Type** | t3.micro |
| **Instance ID** | i-046d8c6492a4cd3fc |
| **Elastic IP** | 3.109.40.217 |
| **Security Group** | sg-00d3152eb15bcaaa5 |
| **Database** | Neon DB PostgreSQL |
| **Cache** | Upstash Redis |
| **Schedule** | 9 AM - 10 PM IST |
| **CI/CD** | GitHub Actions |

---

## 🎉 Deployment Complete!

Your OneQlick backend is now:
- ✅ Running on AWS EC2 Mumbai
- ✅ Accessible at http://3.109.40.217:8000/api/v1
- ✅ Auto-deploying on git push
- ✅ Auto-starting at 9 AM IST
- ✅ Auto-stopping at 10 PM IST
- ✅ Cost-optimized for $100 credits

**Next Steps:**
1. Test all API endpoints
2. Update mobile apps with new API URL
3. Monitor logs and performance
4. Set up domain and SSL (optional)

For issues or questions, check the logs or refer to this guide!
