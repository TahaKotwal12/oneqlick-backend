from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, DECIMAL, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import VehicleType, AvailabilityStatus


class DeliveryPartner(Base):
    """Delivery partner details model."""
    __tablename__ = 'core_mstr_one_qlick_delivery_partners_tbl'

    delivery_partner_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id', ondelete='CASCADE'))
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    vehicle_number = Column(String(50), nullable=False)
    license_number = Column(String(50), nullable=False)
    current_latitude = Column(DECIMAL(10, 8))
    current_longitude = Column(DECIMAL(11, 8))
    availability_status = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.OFFLINE)
    rating = Column(DECIMAL(3, 2), default=0)
    total_ratings = Column(Integer, default=0)
    total_deliveries = Column(Integer, default=0)
    documents_json = Column(JSONB)  # Store document URLs
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
