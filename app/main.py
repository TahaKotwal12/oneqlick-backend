from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.api.exception import EngageFatalException, EngageNonFatalException
from app.api.schemas.common_schemas import CommonResponse
from app.config.logger import get_logger

# Import auth routes
from app.api.routes.auth_controller import router as auth_router

app = FastAPI(title="OneQlick Food Delivery API")

# Include API routes
app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "OneQlick Food Delivery API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "OneQlick Food Delivery API"}

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