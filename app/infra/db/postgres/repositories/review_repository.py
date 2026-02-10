from sqlalchemy.orm import Session
from app.infra.db.postgres.models.review_form import ReviewForm
from app.infra.db.postgres.models.review_response import ReviewResponse
from typing import Optional

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_form_by_slug(self, slug: str) -> Optional[ReviewForm]:
        return self.db.query(ReviewForm).filter(
            ReviewForm.slug == slug,
            ReviewForm.is_active == True
        ).first()

    def create_form(self, title, slug, fields, description=None):
        db_form = ReviewForm(
            title=title,
            slug=slug,
            fields=fields,
            description=description
        )
        self.db.add(db_form)
        self.db.commit()
        self.db.refresh(db_form)
        return db_form

    def create_response(self, user_id, form_id, data):
        db_response = ReviewResponse(
            user_id=user_id,
            form_id=form_id,
            response_data=data
        )
        self.db.add(db_response)
        self.db.commit()
        return db_response