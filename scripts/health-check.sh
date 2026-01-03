#!/bin/bash
# Health check script for Docker container
# Returns 0 if healthy, 1 if unhealthy

set -e

# Configuration
HOST="${HOST:-localhost}"
PORT="${PORT:-8000}"
HEALTH_ENDPOINT="/health"

# Make request to health endpoint
response=$(curl -sf "http://${HOST}:${PORT}${HEALTH_ENDPOINT}" || echo "failed")

# Check if response contains "healthy"
if echo "$response" | grep -q "healthy"; then
    echo "✓ Health check passed"
    exit 0
else
    echo "✗ Health check failed"
    exit 1
fi
