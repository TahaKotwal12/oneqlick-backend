from fastapi import HTTPException
from app.infra.db.postgres.repositories.review_repository import ReviewRepository
from app.api.schemas.review_schemas import ReviewSubmission

class ReviewService:
    def __init__(self, repo: ReviewRepository):
        self.repo = repo

    def get_form(self, slug: str):
        form = self.repo.get_form_by_slug(slug)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        return form

    def create_form(self, title, slug, fields, description=None, status="published"):
        # Check if slug already exists
        existing = self.repo.get_form_by_slug(slug)
        if existing:
            raise HTTPException(status_code=400, detail=f"Form with slug '{slug}' already exists")
        return self.repo.create_form(title, slug, fields, description, status)

    def list_forms(self, include_inactive=False):
        return self.repo.list_forms(include_inactive)

    def update_form(self, form_id, update_data):
        form = self.repo.update_form(form_id, update_data)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        return form

    def delete_form(self, form_id):
        success = self.repo.delete_form(form_id)
        if not success:
            raise HTTPException(status_code=404, detail="Form not found")
        return True

    def submit_review(self, user_id, submission: ReviewSubmission):
        form = self.get_form(submission.slug)
        return self.repo.create_response(user_id, form.id, submission.response_data)

    def get_responses(self, form_id=None):
        return self.repo.get_responses(form_id)