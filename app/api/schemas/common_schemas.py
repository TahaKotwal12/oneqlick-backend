from pydantic import BaseModel
from typing import TypeVar, Generic, Optional
from uuid import UUID

# Generic type for response data
T = TypeVar('T')

class CommonResponse(BaseModel, Generic[T]):
    """
    Standard response format for all OneQlick API endpoints.
    """
    code: int
    message: str
    message_id: str
    data: T

class CommonHeaders(BaseModel):
    """
    Common headers for OneQlick API requests.
    For user APIs, no special headers are required.
    """
    pass

def get_common_headers() -> CommonHeaders:
    """
    Dependency to get common headers.
    For user API, returns empty headers.
    """
    return CommonHeaders()