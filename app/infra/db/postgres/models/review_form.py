from sqlalchemy import Column, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.infra.db.postgres.base import Base
import uuid

class ReviewForm(Base):
    __tablename__ = "core_mstr_one_qlick_review_forms_tbl"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String, unique=True, index=True, nullable=False) # e.g., "profile-rate-app"
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    fields = Column(JSONB, nullable=False) # Stores the JSON schema
    status = Column(String, default="published") # draft, published, archived
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=text("now()"))