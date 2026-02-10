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

    def create_form(self, title, slug, fields, description):
        return self.repo.create_form(title, slug, fields, description)

    def submit_review(self, user_id, submission: ReviewSubmission):
        form = self.get_form(submission.slug)
        return self.repo.create_response(user_id, form.id, submission.response_data)