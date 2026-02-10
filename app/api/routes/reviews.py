from fastapi import APIRouter, Depends, status, Body, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user, require_admin
from app.infra.db.postgres.repositories.review_repository import ReviewRepository
from app.services.review_service import ReviewService
from app.api.schemas.review_schemas import ReviewFormResponse, ReviewFormAdminResponse, ReviewFormCreate, ReviewFormUpdate, ReviewSubmission
from app.api.schemas.common_schemas import CommonResponse
from typing import List
from uuid import UUID

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def get_service(db: Session = Depends(get_db)):
    return ReviewService(ReviewRepository(db))

@router.get("/form/{slug}", response_model=CommonResponse[ReviewFormResponse])
def get_review_form(slug: str, service: ReviewService = Depends(get_service)):
    data = service.get_form(slug)
    return CommonResponse(
        code=status.HTTP_200_OK,
        message="Review form retrieved successfully",
        message_id="REVIEW_FORM_RETRIEVED",
        data=data
    )

@router.post("/response", status_code=status.HTTP_201_CREATED, response_model=CommonResponse[dict])
def submit_review(
    submission: ReviewSubmission,
    service: ReviewService = Depends(get_service),
    current_user = Depends(get_current_user)
):
    service.submit_review(current_user.user_id, submission)
    return CommonResponse(
        code=status.HTTP_201_CREATED,
        message="Review submitted successfully",
        message_id="REVIEW_SUBMITTED",
        data={}
    )

# ============================================
# Admin Management Routes
# ============================================

@router.get("/admin/forms", response_model=CommonResponse[List[ReviewFormAdminResponse]])
def list_review_forms(
    include_inactive: bool = Query(False),
    service: ReviewService = Depends(get_service),
    admin = Depends(require_admin)
):
    data = service.list_forms(include_inactive)
    return CommonResponse(
        code=status.HTTP_200_OK,
        message="Review forms retrieved successfully",
        message_id="REVIEW_FORMS_LISTED",
        data=data
    )

@router.post("/form", status_code=status.HTTP_201_CREATED, response_model=CommonResponse[ReviewFormAdminResponse])
def create_review_form(
    form_data: ReviewFormCreate,
    service: ReviewService = Depends(get_service),
    admin = Depends(require_admin)
):
    data = service.create_form(
        title=form_data.title, 
        slug=form_data.slug, 
        fields=[f.model_dump() for f in form_data.fields], 
        description=form_data.description,
        status=form_data.status
    )
    return CommonResponse(
        code=status.HTTP_201_CREATED,
        message="Review form created successfully",
        message_id="REVIEW_FORM_CREATED",
        data=data
    )

@router.put("/form/{form_id}", response_model=CommonResponse[ReviewFormAdminResponse])
def update_review_form(
    form_id: UUID,
    update_data: ReviewFormUpdate,
    service: ReviewService = Depends(get_service),
    admin = Depends(require_admin)
):
    data = service.update_form(form_id, update_data.model_dump(exclude_unset=True))
    return CommonResponse(
        code=status.HTTP_200_OK,
        message="Review form updated successfully",
        message_id="REVIEW_FORM_UPDATED",
        data=data
    )

@router.delete("/form/{form_id}", response_model=CommonResponse[dict])
def delete_review_form(
    form_id: UUID,
    service: ReviewService = Depends(get_service),
    admin = Depends(require_admin)
):
    service.delete_form(form_id)
    return CommonResponse(
        code=status.HTTP_200_OK,
        message="Review form archived successfully",
        message_id="REVIEW_FORM_ARCHIVED",
        data={}
    )

@router.get("/admin/responses", response_model=CommonResponse[List[dict]])
def get_review_responses(
    form_id: UUID = Query(None),
    service: ReviewService = Depends(get_service),
    admin = Depends(require_admin)
):
    # Note: Returning raw dicts for now as response_data is JSONB
    data = service.get_responses(form_id)
    return CommonResponse(
        code=status.HTTP_200_OK,
        message="Review responses retrieved successfully",
        message_id="REVIEW_RESPONSES_RETRIEVED",
        data=[{
            "id": r.id,
            "user_id": r.user_id,
            "form_id": r.form_id,
            "response_data": r.response_data,
            "created_at": r.created_at
        } for r in data]
    )
