from fastapi import APIRouter, Depends, status, Body
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.infra.db.postgres.repositories.review_repository import ReviewRepository
from app.services.review_service import ReviewService
from app.api.schemas.review_schemas import ReviewFormResponse, ReviewSubmission

from app.api.schemas.common_schemas import CommonResponse

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

@router.post("/form", status_code=status.HTTP_201_CREATED, response_model=CommonResponse[ReviewFormResponse])
def create_review_form(
    title: str = Body(...),       
    slug: str = Body(...),        
    fields: list[dict] = Body(...), 
    description: str = Body(None), 
    service: ReviewService = Depends(get_service),
    # current_user = Depends(get_current_admin_user) # TODO: Protect this!
):
    data = service.create_form(title, slug, fields, description)
    return CommonResponse(
        code=status.HTTP_201_CREATED,
        message="Review form created successfully",
        message_id="REVIEW_FORM_CREATED",
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