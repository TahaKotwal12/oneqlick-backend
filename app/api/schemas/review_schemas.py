from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from uuid import UUID

class ReviewField(BaseModel):
    id: Optional[str] = None
    type: str # 'star_rating', 'text_area'
    label: str
    required: bool = False
    validation: Optional[Dict[str, Any]] = None

class ReviewFormResponse(BaseModel):
    id: UUID
    slug: str
    title: str
    description: Optional[str]
    fields: List[ReviewField]
    created_at: Any

    class Config:
        from_attributes = True

class ReviewFormCreate(BaseModel):
    title: str
    slug: str
    fields: List[ReviewField]
    description: Optional[str] = None
    status: Optional[str] = "published"

class ReviewFormUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    fields: Optional[List[ReviewField]] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class ReviewFormAdminResponse(ReviewFormResponse):
    status: str
    is_active: bool
    updated_at: Any

class ReviewSubmission(BaseModel):
    slug: str # "profile-rate-app"
    response_data: Dict[str, Any]
