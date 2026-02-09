from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import text
from app.infra.db.postgres.base import Base
import uuid

class ReviewResponse(Base):
    __tablename__ = "review_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("core_mstr_one_qlick_users_tbl.user_id"), nullable=False, index=True)
    form_id = Column(UUID(as_uuid=True), ForeignKey("review_forms.id"), nullable=False)
    response_data = Column(JSONB, nullable=False) # Stores user answers
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))