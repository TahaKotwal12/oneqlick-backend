from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.api.exception import EngageFatalException, EngageNonFatalException
from app.api.schemas.common_schemas import CommonResponse
from app.config.logger import get_logger
from app.infra.db.postgres.postgres_config import get_db
from app.infra.redis.repositories.redis_repositories import RedisRepository
from app.api.routes import auth, user, restaurant
# Import models to ensure they are registered with SQLAlchemy
from app.infra.db.postgres.models import user as user_model, address, otp_verification, pending_user, restaurant as restaurant_model, restaurant_offer
# Import batch cleanup worker
from app.workers.batch_cleanup_worker import start_batch_cleanup_worker, stop_batch_cleanup_worker, get_worker_status
import logging

APP_TITLE = "OneQlick Backend"
app = FastAPI(title=APP_TITLE)

# Include API routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(restaurant.router, prefix="/api/v1")

# Initialize Redis connection
try:
    redis_repo = RedisRepository()
    logger = get_logger(__name__)
    logger.info("Redis connection initialized successfully")
except Exception as e:
    logger = get_logger(__name__)
    logger.warning(f"Redis connection failed: {e}")
    redis_repo = None

# Startup event - Initialize batch cleanup service
@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    logger = get_logger(__name__)
    try:
        # Start batch cleanup worker
        start_batch_cleanup_worker()
        logger.info("Batch cleanup service started successfully")
    except Exception as e:
        logger.error(f"Failed to start batch cleanup service: {e}")

# Shutdown event - Clean up services
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up services on application shutdown."""
    logger = get_logger(__name__)
    try:
        # Stop batch cleanup worker
        stop_batch_cleanup_worker()
        logger.info("Batch cleanup service stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping batch cleanup service: {e}")

@app.get("/")
async def root():
    return {
        "message": APP_TITLE, 
        "status": "running",
        "port": 8001,
        "batch_cleanup": "enabled",
        "endpoints": {
            "health": "/health",
            "api_docs": "/docs",
            "batch_cleanup_status": "/api/v1/batch-cleanup/status",
            "batch_cleanup_run": "/api/v1/batch-cleanup/run"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint that verifies database and Redis connections"""
    health_status = {
        "status": "healthy",
        "service": APP_TITLE,
        "database": "unknown",
        "redis": "unknown",
        "batch_cleanup": "unknown"
    }
    
    # Check database connection
    try:
        from sqlalchemy import text
        db = next(get_db())
        db.execute(text("SELECT 1"))
        health_status["database"] = "connected"
        db.close()
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check Redis connection
    try:
        if redis_repo and redis_repo._redis_client:
            redis_repo._redis_client.ping()
            health_status["redis"] = "connected"
        else:
            health_status["redis"] = "not_configured"
    except Exception as e:
        health_status["redis"] = f"error: {str(e)}"
    
    # Check batch cleanup service
    try:
        cleanup_status = get_worker_status()
        if cleanup_status["worker_running"] and cleanup_status["cleanup_service_status"]["running"]:
            health_status["batch_cleanup"] = "running"
        else:
            health_status["batch_cleanup"] = "stopped"
    except Exception as e:
        health_status["batch_cleanup"] = f"error: {str(e)}"
    
    return health_status

@app.get("/api/v1/batch-cleanup/status")
async def batch_cleanup_status():
    """Get the status of the batch cleanup service."""
    try:
        status = get_worker_status()
        return {
            "status": "success",
            "data": {
                "worker_running": status["worker_running"],
                "cleanup_service": status["cleanup_service_status"],
                "message": "Batch cleanup service status retrieved successfully"
            }
        }
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error getting batch cleanup status: {e}")
        return {
            "status": "error",
            "message": f"Failed to get batch cleanup status: {str(e)}"
        }

@app.post("/api/v1/batch-cleanup/run")
async def run_batch_cleanup():
    """Manually trigger batch cleanup."""
    try:
        from app.services.batch_cleanup_service import run_cleanup_now
        deleted_count = run_cleanup_now()
        return {
            "status": "success",
            "data": {
                "deleted_count": deleted_count,
                "message": f"Batch cleanup completed. Deleted {deleted_count} records."
            }
        }
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error running batch cleanup: {e}")
        return {
            "status": "error",
            "message": f"Failed to run batch cleanup: {str(e)}"
        }

@app.exception_handler(EngageFatalException)
async def fatal_exception_handler(request, exc: EngageFatalException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=CommonResponse[dict](
            code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            message=exc.detail, 
            message_id="0", 
            data={}
        ).model_dump()
    )

@app.exception_handler(EngageNonFatalException)
async def non_fatal_exception_handler(request, exc: EngageNonFatalException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=CommonResponse[dict](
            code=status.HTTP_400_BAD_REQUEST, 
            message=exc.detail, 
            message_id="0", 
            data={}
        ).model_dump()
    )

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle FastAPI request validation errors by converting them to our custom format.
    """
    logger = get_logger(__name__)
    first_error = exc.errors()[0]  
    location_parts = [str(loc) for loc in first_error["loc"]]

    if location_parts[0] == "body":
        location_parts.pop(0)

    location = ".".join(location_parts)  
    message = f"{location}: {first_error['msg']}"  

    logger.error(f"Request validation error: {message}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=CommonResponse[dict](
            code=status.HTTP_400_BAD_REQUEST,
            message=message,  
            message_id="0",
            data={}
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """
    Handle all other exceptions.
    """
    logger = get_logger(__name__)
    error_message = str(exc)
    logger.error(f"Unexpected error: {error_message}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=CommonResponse[dict](
            code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            message=f"An unexpected error occurred: {error_message}", 
            message_id="0", 
            data={}
        ).model_dump()
    )
