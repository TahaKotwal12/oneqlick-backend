# OneQlick Backend - Docker Guide

Complete guide for using Docker with the OneQlick backend.

## Quick Start

### Build and Run Locally

```bash
# Build the Docker image
docker build -t oneqlick-backend .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL="your_database_url" \
  -e JWT_SECRET_KEY="your_jwt_secret" \
  oneqlick-backend
```

### Using Docker Compose (Recommended for Development)

```bash
# Start all services (app, postgres, redis)
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Docker Commands Reference

### Building Images

```bash
# Build with default tag
docker build -t oneqlick-backend .

# Build with specific tag
docker build -t oneqlick-backend:v1.0.0 .

# Build without cache
docker build --no-cache -t oneqlick-backend .

# Build with build arguments
docker build --build-arg PORT=8080 -t oneqlick-backend .
```

### Running Containers

```bash
# Run with environment variables
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e REDIS_HOST="localhost" \
  oneqlick-backend

# Run with env file
docker run -p 8000:8000 --env-file .env oneqlick-backend

# Run in detached mode
docker run -d -p 8000:8000 --name oneqlick-api oneqlick-backend

# Run with volume mounts
docker run -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/uploads:/app/uploads \
  oneqlick-backend
```

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop oneqlick-api

# Start container
docker start oneqlick-api

# Restart container
docker restart oneqlick-api

# Remove container
docker rm oneqlick-api

# View container logs
docker logs oneqlick-api

# Follow logs
docker logs -f oneqlick-api

# Execute command in running container
docker exec -it oneqlick-api bash

# View container stats
docker stats oneqlick-api
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi oneqlick-backend

# Remove unused images
docker image prune

# Tag image
docker tag oneqlick-backend:latest oneqlick-backend:v1.0.0

# Save image to file
docker save oneqlick-backend > oneqlick-backend.tar

# Load image from file
docker load < oneqlick-backend.tar
```

---

## Docker Compose Commands

### Basic Operations

```bash
# Start services
docker-compose up

# Start specific service
docker-compose up app

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart app
```

### Viewing Information

```bash
# View running services
docker-compose ps

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# View logs for specific service
docker-compose logs app

# View service configuration
docker-compose config
```

### Building and Updating

```bash
# Build services
docker-compose build

# Build without cache
docker-compose build --no-cache

# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

### Executing Commands

```bash
# Execute command in service
docker-compose exec app bash

# Run one-off command
docker-compose run app python scripts/generate-secrets.py

# Execute as specific user
docker-compose exec -u appuser app bash
```

---

## Environment Configuration

### Using .env File

Create `.env` file from template:

```bash
cp .env.example .env
# Edit .env with your values
```

Docker Compose automatically loads `.env` file.

### Override for Different Environments

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## Volumes and Data Persistence

### Named Volumes

```bash
# Create volume
docker volume create oneqlick-data

# List volumes
docker volume ls

# Inspect volume
docker volume inspect oneqlick-data

# Remove volume
docker volume rm oneqlick-data

# Remove unused volumes
docker volume prune
```

### Backup and Restore

```bash
# Backup PostgreSQL data
docker-compose exec postgres pg_dump -U oneqlick oneqlick_db > backup.sql

# Restore PostgreSQL data
docker-compose exec -T postgres psql -U oneqlick oneqlick_db < backup.sql

# Backup volume
docker run --rm -v oneqlick_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup.tar.gz /data

# Restore volume
docker run --rm -v oneqlick_postgres_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/postgres-backup.tar.gz -C /
```

---

## Networking

### Docker Compose Networks

Services in docker-compose can communicate using service names:

```python
# In your app, use service name as host
DATABASE_URL = "postgresql://user:pass@postgres:5432/db"
REDIS_HOST = "redis"
```

### Custom Networks

```bash
# Create network
docker network create oneqlick-net

# Run container on network
docker run --network oneqlick-net oneqlick-backend

# Connect container to network
docker network connect oneqlick-net oneqlick-api

# Disconnect from network
docker network disconnect oneqlick-net oneqlick-api

# Inspect network
docker network inspect oneqlick-net
```

---

## Debugging

### Access Container Shell

```bash
# Using docker-compose
docker-compose exec app bash

# Using docker
docker exec -it oneqlick-api bash
```

### View Application Logs

```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f app

# Last 100 lines
docker-compose logs --tail=100 app

# Logs since timestamp
docker-compose logs --since 2024-01-03T12:00:00 app
```

### Check Health Status

```bash
# View health status
docker inspect --format='{{.State.Health.Status}}' oneqlick-api

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' oneqlick-api
```

### Test Database Connection

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U oneqlick -d oneqlick_db

# Run SQL query
docker-compose exec postgres psql -U oneqlick -d oneqlick_db -c "SELECT 1"
```

### Test Redis Connection

```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# Ping Redis
docker-compose exec redis redis-cli ping
```

---

## Performance Optimization

### Multi-stage Builds

The Dockerfile uses multi-stage builds to reduce image size:

```dockerfile
# Builder stage - includes build tools
FROM python:3.13-slim AS builder
# ... build dependencies

# Runtime stage - only runtime dependencies
FROM python:3.13-slim
# ... copy from builder
```

### Layer Caching

Optimize build time by ordering Dockerfile commands:

1. Install system dependencies (changes rarely)
2. Copy requirements.txt and install Python packages
3. Copy application code (changes frequently)

### Resource Limits

```bash
# Limit memory
docker run -m 512m oneqlick-backend

# Limit CPU
docker run --cpus=2 oneqlick-backend

# In docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 512M
```

---

## Security Best Practices

### Non-root User

The Dockerfile runs as non-root user `appuser`:

```dockerfile
USER appuser
```

### Secrets Management

**Never commit secrets to Git!**

```bash
# Use environment variables
docker run -e JWT_SECRET_KEY="$(cat secret.txt)" oneqlick-backend

# Use Docker secrets (Swarm mode)
echo "my-secret" | docker secret create jwt_secret -
```

### Scan for Vulnerabilities

```bash
# Scan image
docker scan oneqlick-backend

# Use Trivy
trivy image oneqlick-backend
```

---

## Production Deployment

### Build for Production

```bash
# Build optimized image
docker build -t oneqlick-backend:prod .

# Test production image
docker run -p 8000:8000 --env-file .env.prod oneqlick-backend:prod
```

### Push to Registry

```bash
# Docker Hub
docker tag oneqlick-backend:prod username/oneqlick-backend:latest
docker push username/oneqlick-backend:latest

# AWS ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag oneqlick-backend:prod <account>.dkr.ecr.<region>.amazonaws.com/oneqlick-backend:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/oneqlick-backend:latest
```

---

## Troubleshooting

### Container Exits Immediately

```bash
# Check logs
docker logs oneqlick-api

# Common issues:
# - Missing environment variables
# - Database connection failed
# - Port already in use
```

### Cannot Connect to Database

```bash
# Check if postgres is running
docker-compose ps postgres

# Check postgres logs
docker-compose logs postgres

# Test connection
docker-compose exec app python -c "from app.config.config import DATABASE_URL; print(DATABASE_URL)"
```

### Port Already in Use

```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Use different port
docker run -p 8080:8000 oneqlick-backend
```

### Out of Disk Space

```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

---

## Useful Tips

### Faster Rebuilds

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t oneqlick-backend .
```

### View Image Layers

```bash
# Show image history
docker history oneqlick-backend

# Use dive for detailed analysis
dive oneqlick-backend
```

### Copy Files from Container

```bash
# Copy logs from container
docker cp oneqlick-api:/app/logs ./local-logs

# Copy to container
docker cp local-file.txt oneqlick-api:/app/
```

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)
