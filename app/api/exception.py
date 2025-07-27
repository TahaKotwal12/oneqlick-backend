from fastapi import HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import ValidationError

from app.config.logger import get_logger

logger = get_logger(__name__)

class EngageFatalException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)

class EngageNonFatalException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

class EngageValidationException(HTTPException):
    """
    Custom exception for handling Pydantic validation errors.
    This allows us to convert Pydantic ValidationError to our custom exception format.
    """
    def __init__(self, validation_error: Optional[ValidationError] = None, message: Optional[str] = None):
        if validation_error:
            # Format the validation error details
            error_messages = []
            for error in validation_error.errors():
                message = f"{error['msg']}"
                error_messages.append(message)
    
            detail = f"{error_messages}"
        else:
            # Use the provided message if no validation error is provided
            detail = message or "Validation error occurred"
        
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

def handle_pydantic_validation_error(validation_error: ValidationError) -> EngageValidationException:
    """
    Helper function to convert a Pydantic ValidationError to an EngageValidationException.
    
    Args:
        validation_error: The Pydantic ValidationError
        
    Returns:
        An EngageValidationException with formatted error details
    """
    return EngageValidationException(validation_error=validation_error)
