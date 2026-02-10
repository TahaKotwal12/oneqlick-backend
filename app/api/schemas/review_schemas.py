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

    class Config:
        from_attributes = True

class ReviewSubmission(BaseModel):
    slug: str # "profile-rate-app"
    response_data: Dict[str, Any]
