# OneQlick Backend - Deployment Guide

Complete guide for deploying the OneQlick FastAPI backend to Railway or AWS.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Railway Deployment](#railway-deployment)
- [AWS ECS Deployment](#aws-ecs-deployment)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Health Checks](#health-checks)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools

- **Docker** (v20.10+)
- **Git**
- **Python** 3.13+ (for local testing)

### For Railway Deployment
- Railway account ([railway.app](https://railway.app))
- Railway CLI (optional but recommended)

### For AWS Deployment
- AWS account
- AWS CLI configured
- Docker Hub or AWS ECR account

---

## Railway Deployment

Railway is the **easiest and recommended** option for quick deployment.

### Method 1: Deploy via Railway Dashboard (Easiest)

1. **Push your code to GitHub**
   ```bash
   cd "c:\Users\kotwa\OneDrive\Desktop\ONEQLICK 2026\oneqlick-backend"
   git add .
   git commit -m "Add Docker configuration"
   git push origin main
   ```

2. **Create new project on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `oneqlick-backend` repository

3. **Add PostgreSQL database**
   - In your Railway project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically provision a database

4. **Add Redis (optional)**
   - Click "New" → "Database" → "Redis"

5. **Configure environment variables**
   - Go to your backend service
   - Click "Variables" tab
   - Add the following variables:

   ```env
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_HOST=${{Redis.REDIS_HOST}}
   REDIS_PORT=${{Redis.REDIS_PORT}}
   SECRET_KEY=<generate using scripts/generate-secrets.py>
   JWT_SECRET_KEY=<generate using scripts/generate-secrets.py>
   APP_ENV=production
   DEBUG=false
   PORT=8000
   ```

6. **Deploy**
   - Railway will automatically build and deploy your Docker container
   - Monitor the build logs
   - Once deployed, you'll get a public URL like `https://oneqlick-backend-production.up.railway.app`

### Method 2: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   cd "c:\Users\kotwa\OneDrive\Desktop\ONEQLICK 2026\oneqlick-backend"
   railway init
   ```

4. **Add PostgreSQL**
   ```bash
   railway add --database postgres
   ```

5. **Add Redis**
   ```bash
   railway add --database redis
   ```

6. **Set environment variables**
   ```bash
   # Generate secrets first
   python scripts/generate-secrets.py
   
   # Set variables
   railway variables set SECRET_KEY=<your-secret-key>
   railway variables set JWT_SECRET_KEY=<your-jwt-secret>
   railway variables set APP_ENV=production
   railway variables set DEBUG=false
   ```

7. **Deploy**
   ```bash
   railway up
   ```

8. **Get your deployment URL**
   ```bash
   railway domain
   ```

---

## AWS ECS Deployment

For production-grade deployment with more control.

### Step 1: Create ECR Repository

```bash
# Set variables
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=<your-account-id>
ECR_REPO_NAME=oneqlick-backend

# Create ECR repository
aws ecr create-repository \
    --repository-name $ECR_REPO_NAME \
    --region $AWS_REGION
```

### Step 2: Build and Push Docker Image

```bash
# Build image
cd "c:\Users\kotwa\OneDrive\Desktop\ONEQLICK 2026\oneqlick-backend"
docker build -t oneqlick-backend:latest .

# Tag for ECR
docker tag oneqlick-backend:latest \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Push image
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest
```

### Step 3: Create RDS PostgreSQL Database

```bash
# Create DB subnet group (if not exists)
aws rds create-db-subnet-group \
    --db-subnet-group-name oneqlick-db-subnet \
    --db-subnet-group-description "OneQlick DB Subnet Group" \
    --subnet-ids subnet-xxxxx subnet-yyyyy

# Create PostgreSQL instance
aws rds create-db-instance \
    --db-instance-identifier oneqlick-postgres \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 16.1 \
    --master-username oneqlick \
    --master-user-password <your-secure-password> \
    --allocated-storage 20 \
    --db-subnet-group-name oneqlick-db-subnet \
    --vpc-security-group-ids sg-xxxxx \
    --publicly-accessible
```

### Step 4: Create ElastiCache Redis (Optional)

```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id oneqlick-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1
```

### Step 5: Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name oneqlick-cluster
```

### Step 6: Create Task Definition

Create file `aws/task-definition.json` (already created in this setup) and register it:

```bash
aws ecs register-task-definition \
    --cli-input-json file://aws/task-definition.json
```

### Step 7: Create ECS Service

```bash
aws ecs create-service \
    --cluster oneqlick-cluster \
    --service-name oneqlick-backend \
    --task-definition oneqlick-backend:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" \
    --load-balancer targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=oneqlick-backend,containerPort=8000
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Application secret key | Generate with `generate-secrets.py` |
| `JWT_SECRET_KEY` | JWT signing key | Generate with `generate-secrets.py` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `APP_ENV` | Environment | `production` |
| `DEBUG` | Debug mode | `false` |
| `PORT` | Server port | `8000` |
| `WORKERS` | Gunicorn workers | `4` |

See `.env.example` for complete list.

---

## Database Setup

### Initial Schema Setup

If deploying for the first time, you need to create the database schema:

1. **Connect to your database**
   ```bash
   psql $DATABASE_URL
   ```

2. **Run the schema script**
   ```bash
   psql $DATABASE_URL < scripts/script.sql
   ```

3. **Insert sample data (optional)**
   ```bash
   psql $DATABASE_URL < scripts/insert_sample_restaurants.sql
   psql $DATABASE_URL < scripts/insert_sample_food_items.sql
   ```

---

## Health Checks

### Verify Deployment

```bash
# Replace with your deployment URL
DEPLOYMENT_URL=https://your-app.railway.app

# Health check
curl $DEPLOYMENT_URL/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "OneQlick Backend",
#   "database": "connected",
#   "redis": "connected",
#   "batch_cleanup": "running"
# }
```

### Test API Endpoints

```bash
# Root endpoint
curl $DEPLOYMENT_URL/

# API documentation
open $DEPLOYMENT_URL/docs
```

---

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
# Railway
railway logs

# AWS ECS
aws ecs describe-tasks --cluster oneqlick-cluster --tasks <task-id>
aws logs tail /ecs/oneqlick-backend --follow
```

**Common issues:**
- Missing environment variables
- Database connection failed
- Port already in use

### Database Connection Failed

1. **Verify DATABASE_URL format:**
   ```
   postgresql://username:password@host:port/database
   ```

2. **Check database is accessible:**
   ```bash
   psql $DATABASE_URL -c "SELECT 1"
   ```

3. **Verify security groups (AWS):**
   - ECS tasks can reach RDS on port 5432
   - Security group allows inbound PostgreSQL traffic

### Health Check Failing

1. **Check if app is running:**
   ```bash
   docker ps
   ```

2. **Test health endpoint locally:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Check application logs:**
   ```bash
   docker logs <container-id>
   ```

### High Memory Usage

**Reduce Gunicorn workers:**
```env
WORKERS=2  # Instead of 4
```

**Increase container memory (Railway):**
- Go to Settings → Resources
- Increase memory limit

**Increase task memory (AWS):**
```bash
# Update task definition with more memory
aws ecs update-service --cluster oneqlick-cluster \
    --service oneqlick-backend --force-new-deployment
```

---

## Post-Deployment

### Update Frontend Apps

Update the API URL in both frontend apps:

**oneqlick-partner-app/.env:**
```env
EXPO_PUBLIC_API_BASE_URL=https://your-deployment-url.railway.app/api/v1
```

**oneQlick-User-App/.env:**
```env
EXPO_PUBLIC_API_BASE_URL=https://your-deployment-url.railway.app/api/v1
```

### Monitor Your Application

**Railway:**
- Dashboard shows metrics, logs, and deployments
- Set up alerts for downtime

**AWS:**
```bash
# View CloudWatch logs
aws logs tail /ecs/oneqlick-backend --follow

# Monitor ECS service
aws ecs describe-services --cluster oneqlick-cluster \
    --services oneqlick-backend
```

---

## Scaling

### Railway
- Automatic scaling based on traffic
- Upgrade plan for more resources

### AWS ECS
```bash
# Scale to 4 instances
aws ecs update-service --cluster oneqlick-cluster \
    --service oneqlick-backend --desired-count 4
```

---

## Support

For issues or questions:
- Check logs first
- Review environment variables
- Verify database connectivity
- Test health endpoint

**Railway Support:** https://railway.app/help  
**AWS Support:** https://aws.amazon.com/support
