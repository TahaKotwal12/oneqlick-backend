from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class UserFavorite(Base):
    """
    User favorites model — stores restaurants a user has hearted.
    Table: core_mstr_one_qlick_user_favorites_tbl
    """
    __tablename__ = 'core_mstr_one_qlick_user_favorites_tbl'

    favorite_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('core_mstr_one_qlick_users_tbl.user_id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey('core_mstr_one_qlick_restaurants_tbl.restaurant_id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # A user can only favorite a restaurant once
    __table_args__ = (
        UniqueConstraint('user_id', 'restaurant_id', name='uq_user_restaurant_favorite'),
    )
