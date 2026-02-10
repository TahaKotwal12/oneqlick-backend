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

    def create_form(self, title, slug, fields, description=None, status="published"):
        db_form = ReviewForm(
            title=title,
            slug=slug,
            fields=fields,
            description=description,
            status=status
        )
        self.db.add(db_form)
        self.db.commit()
        self.db.refresh(db_form)
        return db_form

    def list_forms(self, include_inactive=False):
        query = self.db.query(ReviewForm)
        if not include_inactive:
            query = query.filter(ReviewForm.is_active == True)
        return query.order_by(ReviewForm.created_at.desc()).all()

    def update_form(self, form_id, update_data):
        db_form = self.db.query(ReviewForm).filter(ReviewForm.id == form_id).first()
        if db_form:
            for key, value in update_data.items():
                if value is not None:
                    setattr(db_form, key, value)
            self.db.commit()
            self.db.refresh(db_form)
        return db_form

    def delete_form(self, form_id):
        db_form = self.db.query(ReviewForm).filter(ReviewForm.id == form_id).first()
        if db_form:
            db_form.is_active = False
            self.db.commit()
            return True
        return False

    def create_response(self, user_id, form_id, data):
        db_response = ReviewResponse(
            user_id=user_id,
            form_id=form_id,
            response_data=data
        )
        self.db.add(db_response)
        self.db.commit()
        return db_response

    def get_responses(self, form_id=None):
        query = self.db.query(ReviewResponse)
        if form_id:
            query = query.filter(ReviewResponse.form_id == form_id)
        return query.order_by(ReviewResponse.created_at.desc()).all()