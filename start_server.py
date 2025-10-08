#!/usr/bin/env python3
"""
Startup script for OneQlick Backend Server with Batch Cleanup

This script starts the FastAPI server on port 8001 with the batch cleanup service.
"""

import uvicorn
import sys
import os
from app.config.logger import get_logger

logger = get_logger(__name__)

def start_server():
    """Start the FastAPI server with batch cleanup service."""
    try:
        logger.info("Starting OneQlick Backend Server with Batch Cleanup Service...")
        logger.info("Server will be available at: http://localhost:8001")
        logger.info("Health check: http://localhost:8001/health")
        logger.info("Batch cleanup status: http://localhost:8001/api/v1/batch-cleanup/status")
        logger.info("Manual cleanup: POST http://localhost:8001/api/v1/batch-cleanup/run")
        logger.info("API docs: http://localhost:8001/docs")
        logger.info("")
        logger.info("Batch cleanup service will start automatically and run every hour.")
        logger.info("Press Ctrl+C to stop the server.")
        logger.info("=" * 60)
        
        # Start the server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
