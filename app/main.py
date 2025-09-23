from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.api.exception import EngageFatalException, EngageNonFatalException
from app.api.schemas.common_schemas import CommonResponse
from app.config.logger import get_logger
from app.infra.db.postgres.postgres_config import get_db
from app.infra.redis.repositories.redis_repositories import RedisRepository
import logging

APP_TITLE = "OneQlick Backend - Clean Startup"
app = FastAPI(title=APP_TITLE)

# Initialize Redis connection
try:
    redis_repo = RedisRepository()
    logger = get_logger(__name__)
    logger.info("Redis connection initialized successfully")
except Exception as e:
    logger = get_logger(__name__)
    logger.warning(f"Redis connection failed: {e}")
    redis_repo = None

@app.get("/")
async def root():
    return {"message": APP_TITLE, "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint that verifies database and Redis connections"""
    health_status = {
        "status": "healthy",
        "service": APP_TITLE,
        "database": "unknown",
        "redis": "unknown"
    }
    
    # Check database connection
    try:
        db = next(get_db())
        db.execute("SELECT 1")
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
    
    return health_status

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
