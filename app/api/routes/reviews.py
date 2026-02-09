from fastapi import APIRouter, Depends, status, Body
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.infra.db.postgres.repositories.review_repository import ReviewRepository
from app.services.review_service import ReviewService
from app.api.schemas.review_schemas import ReviewFormResponse, ReviewSubmission

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def get_service(db: Session = Depends(get_db)):
    return ReviewService(ReviewRepository(db))

@router.get("/form/{slug}", response_model=ReviewFormResponse)
def get_review_form(slug: str, service: ReviewService = Depends(get_service)):
    return service.get_form(slug)

@router.post("/form", status_code=status.HTTP_201_CREATED)
def create_review_form(
    title: str = Body(...),       
    slug: str = Body(...),        
    fields: list[dict] = Body(...), 
    description: str = Body(None), 
    service: ReviewService = Depends(get_service),
    # current_user = Depends(get_current_admin_user) # TODO: Protect this!
):
    return service.create_form(title, slug, fields, description)

@router.post("/response", status_code=status.HTTP_201_CREATED)
def submit_review(
    submission: ReviewSubmission,
    service: ReviewService = Depends(get_service),
    current_user = Depends(get_current_user)
):
    return service.submit_review(current_user.id, submission)